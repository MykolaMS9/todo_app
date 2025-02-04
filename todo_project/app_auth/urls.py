from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import LoginForm

app_name = "app_auth"

"""
URL patterns for authentication views.

This list defines the URL routing for the authentication-related views,
such as signup, signin, and logout. Each URL pattern is associated 
with a specific view and is named for easy reverse URL lookup in templates 
or views.

1. **signup**:
    - Path: "signup/"
    - View: `RegisterView.as_view()`
    - Template: "app_auth/register.html"
    - Purpose: Displays and handles the user registration form.

2. **signin**:
    - Path: "signin/"
    - View: `LoginView.as_view()`
    - Template: "app_auth/login.html"
    - Form: `LoginForm`
    - Purpose: Displays and handles the user login form, and redirects authenticated users to the homepage or dashboard.

3. **logout**:
    - Path: "logout/"
    - View: `LogoutView.as_view()`
    - Template: "app_auth/logout.html"
    - Purpose: Logs out the user and redirects them to the logout confirmation page.

Each URL pattern is named, allowing for easy reference using `reverse()` or in template tags.
"""
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
