from django.core.management.base import BaseCommand

from apps.goods.models import Product
from apps.sales.models import Sale, SaleProduct

from apps.sales.utils.sale_calculation import sale_calculation
from apps.sales.utils.timing import timing

import random


class Command(BaseCommand):
    help = 'Создание скидок на продукты'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        products = random.sample(list(products), random.randint(1, len(products)))
        for product in products:
            sale, created = Sale.objects.update_or_create(
                sale_price=sale_calculation(product),
                date_to=timing(),
            )
            sale.save()
            sale_product, created = SaleProduct.objects.update_or_create(
                product=product,
                sale=sale,
            )
            sale_product.save()
            self.stdout.write(
                    self.style.SUCCESS(f'Создана скидка на продукт: {product.title}')
                )
        self.stdout.write(
            self.style.SUCCESS(f'Скидки на товары успешно созданы!')
        )
