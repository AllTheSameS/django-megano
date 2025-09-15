from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Удаление всех объектов указанной модели'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Имя модели в формате app.Model')

    def handle(self, *args, **options):
        try:
            # Получаем модель
            app_label, model_name = options['model_name'].split('.')
            model = apps.get_model(app_label, model_name)

            # Подсчитываем и удаляем
            count = model.objects.count()

            if count == 0:
                self.stdout.write(self.style.WARNING('Нет объектов для удаления'))
                return

            # Подтверждение
            confirm = input(f'Удалить {count} объектов модели {model_name}? (y/N): ')
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING('Удаление отменено'))
                return

            # Удаление
            deleted_count = model.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'Удалено {deleted_count} объектов'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {str(e)}'))