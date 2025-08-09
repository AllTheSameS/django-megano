from django.urls import path, include
from .views import SignInView, SignUpView
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = "myauth"

router = routers.DefaultRouter()

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="login"),
    path("sign-up/", SignUpView.as_view(), name="register"),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
