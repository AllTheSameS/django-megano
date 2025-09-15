from django.urls import path
from .views import ProductDetailsView, ProductView, ProductPopularView, ProductLimitedView

app_name = 'goods'

urlpatterns = [
    path('catalog', ProductView.as_view(), name='product_catalog',),
    path('product/<int:id>', ProductDetailsView.as_view(), name='product_details'),
    path('products/popular', ProductPopularView.as_view(), name='popular_products'),
    path('products/limited', ProductLimitedView.as_view(), name='limited_products'),
]