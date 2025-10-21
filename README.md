# Megano — дипломный проект

Монорепозиторий с бэкендом на Django (проект megano) и фронтенд‑приложением (Django templates + static) для интернет‑магазина. Реализованы аутентификация, каталог с фильтрами и сортировкой, корзина, заказы, отзывы, акции, платежи, а также спецификация API в формате OpenAPI/Swagger.

Этот файл описывает запуск, конфигурацию окружения, основные команды и структуру проекта.

## Содержание
- Возможности
- Технологии
- Структура репозитория
- Быстрый старт
- Конфигурация (.env)
- Бэкенд: управление и запуск
- Фронтенд: управление и запуск
- База данных и миграции
- Демоданные (fixtures/management commands)
- Документация API (Swagger/OpenAPI)
- Тестирование
- Стиль кода и качество
- Пакетирование фронтенда
- Частые проблемы

## Возможности
- Пользовательские аккаунты (регистрация, вход, профиль) с валидаторами и логированием
- Каталог товаров с фильтрами/сортировкой (utils в apps/goods)
- Модули баннеров, отзывов, акций
- Корзина и заказы со статусами и процессом оплаты
- Подключаемые платёжные сервисы (apps/payment/services)
- Админ‑панель для всех приложений
- Статическая спецификация OpenAPI (swagger/swagger.yaml)

## Технологии
- Python 3.10+
- Django 4.x
- База данных: SQLite/PostgreSQL (через Django ORM)
- Внутренние сериализаторы (похоже на DRF‑подход)
- OpenAPI/Swagger для описания API

## Структура репозитория
- diploma-backend/megano
  - megano/ — проект Django (settings, urls, wsgi/asgi)
  - apps/ — приложения:
    - banners, basket, characteristics, goods, myauth, orders, payment, reviews, sales, utils
    - в каждом: models, serializers, views, urls, admin, migrations, tests
  - media/ — загрузки во время работы
  - manage.py
- diploma-frontend/
  - frontend/ — Django‑приложение с шаблонами и статикой
  - swagger/swagger.yaml — спецификация API
  - setup.py, pyproject.toml, MANIFEST.in — файлы упаковки
- .env.template — пример переменных окружения

## Быстрый старт
1) Создайте и активируйте виртуальное окружение (Windows, cmd):

   python -m venv .venv
   .\.venv\Scripts\activate

2) Установите зависимости (из корня репозитория):

   pip install -U pip
   pip install -e ./diploma-frontend
   pip install -r diploma-backend/requirements.txt  (если файл есть)

   Если requirements.txt отсутствует, установите Django напрямую:

   pip install django

3) Создайте файл .env
- Скопируйте .env.template в .env и заполните значения (см. раздел Конфигурация).

4) Примените миграции и создйте суперпользователя:

   cd diploma-backend/megano
   python manage.py migrate
   python manage.py createsuperuser

5) Запустите сервер разработки:

   python manage.py runserver

6) Откройте в браузере:
- API/бэкенд: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/
- Страницы фронтенда (через приложение frontend): http://127.0.0.1:8000/

## Конфигурация (.env)
Файл .env располагайте в корне репозитория или рядом с настройками Django, в зависимости от того, как подключается загрузка переменных. В качестве примера используйте .env.template. Частые переменные:
- DJANGO_SECRET_KEY — секретный ключ Django
- DJANGO_DEBUG — true/false
- DJANGO_ALLOWED_HOSTS — список хостов через запятую (например, 127.0.0.1,localhost)
- DATABASE_URL — например, sqlite:///db.sqlite3 или postgres://user:pass@host:port/db
- MEDIA_ROOT, MEDIA_URL — настройки медиа
- STATIC_ROOT, STATIC_URL — настройки статики
- PAYMENT_* — ключи/параметры платёжных интеграций (п��и необходимости)

Основные настройки находятся в diploma-backend/megano/megano/settings.py. Убедитесь, что .env читается (например, через django-environ). Если нет — задайте параметры непосредственно в settings.py.

## Бэкенд: управление и запуск
Работайте из каталога diploma-backend/megano:
- Запуск сервера:

  python manage.py runserver

- Сбор статики (для продакшена):

  python manage.py collectstatic

- Загрузка фикстур или выполнение кастомных команд (см. Демоданные):

  python manage.py <command>

Обзор приложений (diploma-backend/megano/apps):
- myauth — аутентификация, профиль, валидаторы (apps/myauth/utils/validators.py)
- goods — каталог, фильтрация (apps/goods/utils/filter_and_sort_catalog.py)
- basket, orders — корзина и заказы
- payment — платёжные сервисы (apps/payment/services)
- reviews, sales, banners, characteristics — предметные модули
- utils — общие вспомогательные функции

## База данных и миграции
- Схема и изменения хранятся в migrations каждого приложения.
- Применить все миграции:

  python manage.py migrate

- Создать новые миграции после изменений моделей:

  python manage.py makemigrations
  python manage.py migrate

## Демоданные (fixtures/management commands)
В ряде приложений есть management/commands. Типовое использование:

python manage.py <имя_команды>

Проверьте доступные команды в apps/<app>/management/commands/ (например, goods, characteristics, orders, reviews, sales, myauth). Часто там находятся загрузчики тестовых данных.

Если есть JSON‑фикстуры:

python manage.py loaddata <fixture.json>

## Документациия API (Swagger/OpenAPI)
- Статическая спецификация: diploma-frontend/swagger/swagger.yaml
- Быстрый локальный просмотр через Swagger UI (Docker):

  docker run -p 8080:8080 -e SWAGGER_JSON=/foo/swagger.yaml -v %cd%/diploma-frontend/swagger:/foo swaggerapi/swagger-ui

  Откройте http://127.0.0.1:8080

Либо интегрируйте drf-yasg/drf-spectacular в Django при необходимости.

## Тестирование
Запуск тестов из каталога бэкенда:

python manage.py test

## Стиль кода и качество
В корне есть setup.cfg. Рекомендуемые инструменты:

pip install black isort flake8
black .
isort .
flake8

## Частые проблемы
- Модуль не найден: убедитесь, что установлен фроонтенд‑пакет: pip install -e ./diploma-frontend
- Ошибки миграций: при работе с SQLite можно удалить db.sqlite3 (с осторожностью) и повторить makemigrations/migrate
- Статика не отдается: проверьте STATIC_URL/STATIC_ROOT и выполните collectstatic для продакшена
- Переменные окружения не подхватываются: проверьте чтение .env в settings.py или экспортируйте их в окружение
- Ошибки оплаты: проверьте тестовые ключи и корректность подключения сервисов в apps/payment/services

## Лицензия
Учебный дипломный проект. Используйте по своему усмотрению.
