from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from apps.goods.models import Product, ProductImage
from apps.characteristics.models import Category, Tag, Specification, ProductSpecification
from megano.settings import DEFAULT_PRODUCT_IMAGE_PATH

import random


class Command(BaseCommand):
    help = 'Создание случайного товара'

    def add_arguments(self, parser):
        parser.add_argument('total',
                            type=int,
                            default=10,
                            help='Количество создаваемых товаров',)

    def handle(self, *args, **kwargs):
        try:
            count = kwargs.get('total', 5)

            category_names = [
                "Смартфоны", "Ноутбуки", "Наушники", "Телевизоры",
            ]

            brands = ["Samsung", "Apple", "Sony", "LG", "Xiaomi", "Huawei", "Philips", "Bosch",]

            characteristics = {
                "Смартфон": {
                    "Экран": ["6.1″ OLED", "6.7″ AMOLED", "6.4″ IPS", "120Hz", "90Hz", "60Hz"],
                    "Разрешение": ["Full HD+", "Quad HD+", "4K", "720x1600", "1080x2400"],
                    "Процессор": ["Snapdragon 8 Gen 2", "A16 Bionic", "Exynos 2200", "MediaTek Dimensity 9000"],
                    "Память": ["8/128GB", "12/256GB", "6/64GB", "8/256GB", "12/512GB"],
                    "Аккумулятор": ["5000 mAh", "4500 mAh", "4000 mAh", "быстрая зарядка 65W", "беспроводная зарядка"],
                    "Дополнительно": ["5G", "NFC", "IP68", "стереодинамики", "сканер отпечатка"]
                },
                "Ноутбуки": {
                    "Диагональ экрана": ["13.3″", "14″", "15.6″", "16″", "17.3″"],
                    "Разрешение": ["Full HD", "4K UHD", "QHD", "Retina"],
                    "Процессор": ["Intel Core i7-12700H", "AMD Ryzen 7 6800H", "Apple M2", "Intel Core i5-1240P"],
                    "Видеокарта": ["NVIDIA RTX 4060", "RTX 3070 Ti", "Intel Iris Xe", "AMD Radeon 680M"],
                    "Оперативная память": ["16GB DDR5", "32GB DDR4", "8GB LPDDR5", "64GB DDR5"],
                    "Накопитель": ["1TB SSD NVMe", "512GB SSD", "2TB HDD + 512GB SSD"],
                    "ОС": ["Windows 11", "macOS Ventura", "без ОС", "Linux"],
                    "Батарея": ["до 10 часов", "до 8 часов", "быстрая зарядка"],
                    "Порты": ["USB-C Thunderbolt 4", "HDMI", "USB 3.2", "SD кардридер"],
                    },
                "Наушники": {
                    "Тип": ["беспроводные", "проводные", "накладные", "вкладыши", "полноразмерные"],
                    "Технология": ["Bluetooth 5.2", "3.5mm jack", "USB-C", "Lightning"],
                    "Шумоподавление": ["активное", "пассивное", "прозрачный режим"],
                    "Аккумулятор": ["30 часов работы", "20 часов", "быстрая зарядка 15min=3h"],
                    "Водозащита": ["IPX4", "IPX7", "без защиты"],
                    "Диапазон частот": ["20Hz-20kHz", "10Hz-40kHz"],
                    "Микрофон": ["встроенный", "с шумоподавлением", "съемный"],
                    "Дополнительно": ["кастомный эквалайзер", "мультиподключение", "сенсорное управление"]
                },
                "Телевизор": {
                    "Диагональ": ["43″", "55″", "65″", "75″", "85″"],
                    "Разрешение": ["4K UHD", "8K UHD", "QLED", "OLED"],
                    "HDR": ["HDR10", "Dolby Vision", "HLG", "HDR10+"],
                    "Частота обновления": ["60Hz", "120Hz", "240Hz"],
                    "Smart TV": ["Android TV", "webOS", "Tizen", "Google TV"],
                    "Звук": ["Dolby Atmos", "DTS:X", "20W", "40W", "сабвуфер"],
                    "Порты": ["HDMI 2.1", "eARC", "USB", "Optical audio"],
                    "Дополнительно": ["голосовое управление", "игровой режим", "амбиентный режим"],
                },
            }

            # Получаем категории
            categories = []

            for category_name in category_names:
                category = Category.objects.get(title=category_name)
                categories.append(category)

            # Получаем тэги
            tags = Tag.objects.all()

            # Создаем словарь характеристик для каждой категории
            category_specifications = {}
            for category_name in category_names:
                category_specifications[category_name] = {}

                for spec_name, spec_values in characteristics[category_name].items():
                    spec_obj, created = Specification.objects.get_or_create(name=spec_name)
                    category_specifications[category_name][spec_obj] = spec_values

            created_count = 0
            for _ in range(count):
                random_category = random.choice(categories)
                brand = random.choice(brands)
                product_name = f"{brand} {random_category.title}"

                product = Product(
                    category=random_category,
                    title=product_name,
                    price=random.uniform(100, 10000),
                    count=random.randint(0, 100),
                    description=f"Отличное качество и функциональность.",
                    full_description='Полное описание товара...',
                    free_delivery=random.choice([True, False]),
                    rating=round(random.uniform(1.0, 5.0), 2)
                )

                product.save()

                # Добавляем случайные теги (2-4 тега)
                if tags:
                    random_tags = random.sample(list(tags), random.randint(2, 4))
                    product.tags.set(random_tags)

                # Добавляем характеристики для данной категории
                specs_for_category = category_specifications[random_category.title]
                product_specs = {}

                # Выбираем 3-5 случайных характеристик для этого товара
                selected_specs = random.sample(list(specs_for_category.keys()), min(random.randint(3, 5), len(specs_for_category)))
                for spec in selected_specs:
                    possible_values = specs_for_category[spec]
                    value = random.choice(possible_values)
                    product_specs[spec] = value
                    product_spec = ProductSpecification.objects.create(product=product, specification=spec, value=value)
                    product_spec.save()

                # Добавляем случайное количество картинок (1-5 картинок)
                product_image = [ProductImage.objects.create(product=product, src=DEFAULT_PRODUCT_IMAGE_PATH) for _ in range(random.randint(1, 5))]
                product.images.set(product_image)

                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(f'Создан товар: {product.title} - {round(product.price, 2)} руб.')
                )

            self.stdout.write(
                self.style.SUCCESS(f'Успешно создано {created_count} товаров')
            )
        except Category.DoesNotExist:
            raise ObjectDoesNotExist(
                    'Categories have not been created for these products.'
                )
