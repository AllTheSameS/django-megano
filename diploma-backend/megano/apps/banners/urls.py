from django.urls import path

from .views import BannerView

app_name = 'banners'

urlpatterns = [
    path('banners', BannerView.as_view(), name='banner'),
]