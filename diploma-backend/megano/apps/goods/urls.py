from django.urls import path
from .views import ProductDetailsView

app_name = 'goods'

urlpatterns = [
    path('product/<int:id>', ProductDetailsView.as_view(), name='product_details'),
]
