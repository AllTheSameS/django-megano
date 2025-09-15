from django.core.management.base import BaseCommand

from apps.characteristics.models import Category, CategoryImage


class Command(BaseCommand):
    help = 'Создание категорий'

    def handle(self, *args, **kwargs):
        data = {
            'Смартфоны и гаджеты': [
                'Смартфоны',
                'Наушники',
                'Смарт часы',
            ],
            'Ноутбуки и переферия': [
                'Ноутбуки',
                'Чехлы для ноутбуков',
                'Подставки для ноутбуков',
            ],
            'ТВ': {
                'Телевизоры и аксессуары': [
                    'Телевизоры',
                    'Кронштейны для телевизоров',
                ],
                'Аудиотехника': {
                    'Наушники и гарнитуры': ['Игровые наушники'],
                    'Колонки': ['Умные колонки', '5.1'],
                },
            },
        }


        def create_categories(data, parent=None):
            """
            Рекурсивно создает категории и подкатегории.

            Args:
                data: словарь или список с данными категорий.
                parent: родительская категория (по умолчанию None).
            """
            if isinstance(data, dict):
                for category_name, sub_data in data.items():
                    current_category = Category.objects.create(
                        title=category_name,
                        parent=parent,
                    )
                    CategoryImage.objects.create(
                        category=current_category,
                    )
                    current_category.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Создана категория: {current_category.title}. Родитель: {current_category.parent}')
                    )
                    create_categories(sub_data, current_category)

            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        new_category = Category.objects.create(
                            title=item,
                            parent=parent,
                        )
                        CategoryImage.objects.create(
                            category=new_category,
                            )

                        new_category.save()
        create_categories(data=data)
        self.stdout.write(
            self.style.SUCCESS(f'Категории созданы!')
            )
