from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.orders.models import Order

from .models import Payment

from .services.mock_payment import PaymentService

from megano.settings import PAYMENT_GATEWAY

class PaymentView(APIView):
    """
    Представление работы с оплатой.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, id: int):
        """
        Метод оплаты заказа.

        Attributes:
            id(int): Id заказа.
        """
        try:
            order = Order.objects.get(id=id, customer=request.user)
            if order.status != 'pending':
                return Response({'error': 'This order has already been processed or cancelled.'},
                                status=status.HTTP_400_BAD_REQUEST,)
            payment = Payment.objects.create(
                order=order,
                payment_type=order.payment_type,
            )
            if PAYMENT_GATEWAY == 'mock':
                order.status = 'processing'
                order.save()
                payment_process = PaymentService()
                payment_status, message = payment_process.mock_payment_process_payment(card_data=request.data)
                print(payment_process)
            else:
                PaymentService.payment_process_payment()
            if payment_status:
                payment.status = 'completed'
                order.status = 'paid'
                response = Response(message, status=status.HTTP_200_OK)
            else:
                payment.status = 'failed'
                order.status = 'cancelled'
                response = Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            payment.save()
            order.save()
            print(response)
            return response

        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )