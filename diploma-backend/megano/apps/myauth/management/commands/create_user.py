from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from apps.myauth.models import Profile

import random


class Command(BaseCommand):
    help = 'Создание случайного пользователя'

    def handle(self, *args, **kwargs):
        random_email = f'{get_random_string(5)}@mail.ru'
        random_phone = str(random.randint(0,999999999)).zfill(9)
        user = User.objects.create_user(username=get_random_string(5), password='123')
        Profile.objects.create(
            user=user,
            email=random_email,
            phone=random_phone,
            full_name='test_user',)
        self.stdout.write(
            self.style.SUCCESS(f'Создан пользователь: {user.username}')
        )
        return user.username
