from django.urls import path

from .views import OrderView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('orders', OrderView.as_view(), name='orders'),
    path('order/<int:id>', OrderDetailView.as_view(), name='order_detail'),
]
