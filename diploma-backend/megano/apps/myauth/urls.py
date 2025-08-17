from django.urls import path
from .views import SignInView, SignUpView, signOut, ProfileView, ProfileUpdatePasswordView, ProfileUpdateAvatar

app_name = "myauth"

urlpatterns = [
    path("sign-in", SignInView.as_view(), name="login"),
    path("sign-up", SignUpView.as_view(), name="register"),
    path("sign-out", signOut, name='logout'),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/password", ProfileUpdatePasswordView.as_view(), name="update_password"),
    path("profile/avatar", ProfileUpdateAvatar.as_view(), name="update_avatar")
]
