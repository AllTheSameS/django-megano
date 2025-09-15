import decimal
import random


def sale_calculation(product):
        return product.price * decimal.Decimal((1 - random.choice((10, 20, 30, 40, 50)) / 100))