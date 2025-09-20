import random

from time import sleep


class PaymentService:
    """
    Сервис оплаты заказа.
    """
    def payment_process_payment(self, order_data, card_data):
        """
        Оплата заказа
        """
        pass

    def mock_payment_process_payment(self, card_data):
        """
        Тестовая оплата заказа.
        """
        exceptions = (
            'insufficient_funds',
            'payment_method_limit_exceeded',
            'expired_card',
            'invalid_card_number',
            'transaction_not_permitted',
        )
        sleep(2)
        card_number = int(card_data['number'])
        if card_number % 2 == 0 and card_number % 10 != 0:
            return True, {
                'message': 'Payment successful',
                }
        else:
            return False, {
                'error': random.choice(exceptions),
                }
