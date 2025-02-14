from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

"""
URL patterns for the project, including routes for the admin interface and 
third-party apps (e.g., Todo and authentication).

This list contains the URL routing configuration for the entire project. 
It includes the following:

Path Definitions:
1. **admin**:
    - Path: "/admin/"
    - View: `admin.site.urls`
    - Purpose: Routes to the Django admin site for managing the application (admin.site.urls).
2. **main**:
    - /: Includes the URL patterns from the `todo_app` application (todo_app.urls).
3. **main**:
    - /app_auth/: Includes the URL patterns from the `app_auth` application (app_auth.urls).
4. **MEDIA_URL**:
    - MEDIA_URL: Serves media files during development using Django's static files handler.
"""
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todo_app.urls")),
    path("app_auth/", include("app_auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
