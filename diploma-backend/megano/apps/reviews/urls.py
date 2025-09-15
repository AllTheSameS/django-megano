from django.urls import path

from .views import ReviewView

app_name = 'reviews'

urlpatterns = [
    path('product/<int:id>/reviews', ReviewView.as_view(), name='give_review'),
]
