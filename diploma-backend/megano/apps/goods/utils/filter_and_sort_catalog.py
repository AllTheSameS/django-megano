from django.db.models import Q


class ProductFilterService:
    """Сервисный слой для фильтрации продуктов"""

    @staticmethod
    def build_filters(query_params):
        """
        Метод фильтрации продуктов.

        Attributes:
            title(str): Фильтр по названию (частичное совпадение).
            min_price(int): Минимальная цена.
            max_price(int): Максимальная цена.
            free_delivery(bool): фильтр по бесплатной доставке.
            available(bool): Доступность продукта.
            tags(int): Тэги продукта.
        """
        filters = Q()

        # Фильтр по названию
        if title := query_params.get('filter[name]'):
            filters &= Q(title__icontains=title)

        # Фильтр по цене
        if min_price := query_params.get('filter[minPrice]'):
            try:
                filters &= Q(price__gte=float(min_price))
            except ValueError:
                raise ValueError("minPrice must be a number")

        if max_price := query_params.get('filter[maxPrice]'):
            try:
                filters &= Q(price__lte=float(max_price))
            except ValueError:
                raise ValueError("maxPrice must be a number")

        # Фильтр по доставке
        if free_delivery := query_params.get('filter[freeDelivery]'):
            if free_delivery.lower() == 'true':
                filters &= Q(free_delivery=True)

        # Фильтр по доступности
        if available := query_params.get('filter[available]'):
            if available.lower() == 'true':
                filters &= Q(available=True)
            elif available.lower() == 'false':
                filters &= Q(available=False)

        # Фильтр по тегам
        if tags := query_params.getlist('tags[]'):
            filters &= Q(tags__id__in=tags)

        if category := query_params.getlist('category'):
            filters &= Q(category__id__in=category)
        return filters

    @staticmethod
    def get_sort_params(query_params):
        """
        Метод сортировки продуктов.

        Attributes:
            sort(str): Параметр сортировки.
            sort_type(str): Тип сортировки(Убывание, возрастание)
        """
        sort = query_params.get('sort')
        sort_type = query_params.get('sortType', 'desc')

        if not sort:
            return '-id'  # Сортировка по умолчанию

        if sort == 'reviews':
            sort_field = 'reviews_count'
        else:
            sort_field = sort

        return f'-{sort_field}' if sort_type == 'inc' else sort_field
