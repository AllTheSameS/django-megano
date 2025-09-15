from django.core.management.base import BaseCommand

from apps.characteristics.models import Tag


class Command(BaseCommand):
    help = 'Создание тэгов'

    def handle(self, *args, **kwargs):
        tags_list = ["премиум", "премиум-класс", "элитный", "дизайнерский",
                     "ограниченная серия", "эксклюзив", "роскошный",
                     "премиум-качество",
                    ]
        for tag in tags_list:
            Tag.objects.create(name=tag)
            self.stdout.write(
                self.style.SUCCESS(f'Тэг "{tag}" создан.')
                )
        self.stdout.write(
            self.style.SUCCESS(f'Тэги успешно созданы!')
        )