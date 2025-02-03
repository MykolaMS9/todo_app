from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import LoginForm

app_name = "app_auth"

urlpatterns = [
    path("signup/", views.RegisterView.as_view(), name="signup"),  # app_auth:signup
    path(
        "signin/",
        LoginView.as_view(
            template_name="app_auth/login.html",
            form_class=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="signin",
    ),  # app_auth:signin
    path(
        "logout/",
        LogoutView.as_view(template_name="app_auth/logout.html"),
        name="logout",
    ),  # app_auth:logout
]
