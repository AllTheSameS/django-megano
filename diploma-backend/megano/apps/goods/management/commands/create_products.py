from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from apps.goods.models import Product, Category, ProductImage, Tag, Specification, ProductSpecification

import random


class Command(BaseCommand):
    help = 'Создание случайного товара'

    def add_arguments(self, parser):
        parser.add_argument('total',
                            type=int,
                            default=10,
                            help='Количество создаваемых товаров',)

    def handle(self, *args, **kwargs):
        count = kwargs.get('total', 5)

        category_names = [
            "Смартфон", "Ноутбук", "Наушники", "Телевизор",
        ]

        brands = ["Samsung", "Apple", "Sony", "LG", "Xiaomi", "Huawei", "Philips", "Bosch",]

        tags_list = ["премиум", "премиум-класс", "элитный", "дизайнерский",
                "ограниченная серия", "эксклюзив", "роскошный", "премиум-качество",
                ]
        characteristics = {
            "Смартфон": {
                "Экран": ["6.1″ OLED", "6.7″ AMOLED", "6.4″ IPS", "120Hz", "90Hz", "60Hz"],
                "Разрешение": ["Full HD+", "Quad HD+", "4K", "720x1600", "1080x2400"],
                "Процессор": ["Snapdragon 8 Gen 2", "A16 Bionic", "Exynos 2200", "MediaTek Dimensity 9000"],
                "Память": ["8/128GB", "12/256GB", "6/64GB", "8/256GB", "12/512GB"],
                "Аккумулятор": ["5000 mAh", "4500 mAh", "4000 mAh", "быстрая зарядка 65W", "беспроводная зарядка"],
                "Дополнительно": ["5G", "NFC", "IP68", "стереодинамики", "сканер отпечатка"]
            },
            "Ноутбук": {
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

        # Получаем или создаем категории
        categories = [Category.objects.get_or_create(title=category_name)[0] for category_name in category_names]

        # Получаем или создаем тэги
        tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_list]

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
                rating=random.uniform(1.0, 5.0)
            )

            product.save()

            # Добавляем случайные теги (2-4 тега)
            random_tags = random.sample(tags, random.randint(2, 4))
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
                ProductSpecification.objects.create(product=product, specification=spec, value=value)
            product.specifications.set(product_specs)
            created_count += 1

            self.stdout.write(
                self.style.SUCCESS(f'Создан товар: {product.title} - {product.price} руб.')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {created_count} товаров')
        )