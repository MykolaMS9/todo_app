from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todo_app.urls")),
    path("app_auth/", include("app_auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
