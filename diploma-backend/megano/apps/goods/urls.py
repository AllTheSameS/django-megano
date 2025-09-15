from django.urls import path
from .views import ProductDetailsView, ProductView

app_name = 'goods'

urlpatterns = [
    path('catalog', ProductView.as_view(), name='product_catalog',),
    path('product/<int:id>', ProductDetailsView.as_view(), name='product_details'),
]