from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command

from apps.goods.models import Product
from apps.reviews.models import Review

import random


class Command(BaseCommand):
    help = 'Создание отзывов на продукты'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            users = [User.objects.get(username=call_command('create_user')) for _ in range(random.randint(1, 3))]
            for user in users:
                review = Review.objects.create(
                    product=product,
                    author=user,
                    text='Отзыв',
                    rate=random.randint(1, 5),
                )
                review.save()
            self.stdout.write(
                    self.style.SUCCESS(f'Созданы отзывы на продукт: {product.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Отзывы на товары успешно созданы!')
        )