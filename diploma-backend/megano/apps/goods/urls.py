from django.urls import path
from .views import ProductDetailsView, ProductReviewView, TagsView

app_name = 'goods'

urlpatterns = [
    path('product/<int:id>/reviews', ProductReviewView.as_view(), name='product_review'),
    path('product/<int:id>', ProductDetailsView.as_view(), name='product_details'),
    path('tags', TagsView.as_view(), name='all_tags')
]
