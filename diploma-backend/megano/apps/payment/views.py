from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.orders.models import Order
from apps.utils.utils import BaseView

from .models import Payment

from .services.mock_payment import PaymentService

from megano.settings import PAYMENT_GATEWAY

import logging

logger = logging.getLogger('payment')


class PaymentView(APIView, BaseView):
    """
    Представление работы с оплатой.

    Methods:
        post: Метод оплаты заказа.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, id: int):
        """
        Метод оплаты заказа.

        Attributes:
            request: Метаданные запроса.
            id(int): Id заказа.
        """
        try:
            logger.info('Payment for the order: %s', id)
            order = self._get_order(id=id, user=request.user)
            payment = self._create_payment(order=order)
            self._checking_count_goods(order=order)

            payment_status, message = self._checking_payment_gateway(order=order, data=request.data)

            return self._completing_the_payment(
                payment_status=payment_status,
                message=message,
                order=order,
                payment=payment,
            )

        except ValueError as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_400_BAD_REQUEST,
                logger=logger,
            )
        except Exception as e:
            return self._handle_error(
                message=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                logger=logger,
            )

    def _get_order(self, id: int, user):
        """
        Вспомогательный метод получения заказа.

        Attributes:
            id: Id заказа.
        """
        logger.debug('Get order: %s', id)
        order = Order.objects.get(id=id, customer=user)
        if order.status != 'pending':
            raise ValueError('This order has already been processed or cancelled.')
        return order

    def _create_payment(self, order):
        """
        Создание платежа.

        Attributes:
            order: Заказ.
        """
        logger.debug('Creating a payment for an order: %s', order.id)
        return Payment.objects.create(
                order=order,
                payment_type=order.payment_type,
            )

    def _checking_count_goods(self, order):
        """
        Проверка количества продуктов в заказе.

        Attributes:
            order: Заказ.
        """
        logger.debug('Checking count goods')
        if any([not item.checking_count_goods() for item in order.items.all()]):
            raise ValueError('There are not enough products in the store.')

    def _checking_payment_gateway(self, order, data):
        """
        Проверка платежного шлюза.

        Attributes:
            order: Заказ.
            data: Данные платежа.
        """
        logger.debug('Checking payment gateway')
        if PAYMENT_GATEWAY == 'mock':
                order.status = 'processing'
                order.save()
                payment_process = PaymentService()
                payment_status, message = payment_process.mock_payment_process_payment(card_data=data)
        else:
            payment_status, message = PaymentService.payment_process_payment()
        return payment_status, message

    def _completing_the_payment(self, payment_status, message, payment, order):
        """
        Завершение платежа.

        Attributes:
            payment_status: Статус платежа.
            message: Сообщение.
            payment: Платеж.
            order: Заказ.
        """
        if payment_status:
            payment.status = 'completed'
            order.status = 'paid'
            for item in order.items.all():
                product = item.product
                product.update_shopping_counter(shopping_count=item.count)
                product.update_count(shopping_count=item.count)
                product.save()

            response = Response(message, status=status.HTTP_200_OK)
        else:
            payment.status = 'failed'
            order.status = 'cancelled'
            response = Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        payment.save()
        order.save()
        return response
