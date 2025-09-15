from django.urls import path

from .views import SalesView

app_name = 'sales'

urlpatterns = [
    path('sales', SalesView.as_view(), name='product_sales'),
]