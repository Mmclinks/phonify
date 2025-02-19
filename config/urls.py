"""
Конфигурация URL-маршрутов для проекта Phonify.

Этот модуль определяет пути (URL) проекта, включая:
- Административную панель Django.
- Подключение маршрутов приложения `users`.
- Документацию API с использованием drf-yasg (Swagger и ReDoc).

Используемые пакеты:
- django.urls: для маршрутизации URL.
- drf_yasg: для автоматической генерации документации API.
- rest_framework.permissions: для настройки прав доступа.

Документация API доступна по адресам:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

# Настройка документации API
schema_view = get_schema_view(
    openapi.Info(
        title="Phonify API",
        default_version="v1",
        description="Документация API для авторизации и реферальной системы",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@phonify.com"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

# Определение маршрутов проекта
urlpatterns = [
    path("admin/", admin.site.urls),  # Административная панель Django
    path("", include("users.urls")),  # Подключение маршрутов приложения users
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # Swagger UI документация
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),  # ReDoc документация
]
