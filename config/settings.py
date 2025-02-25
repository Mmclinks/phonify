import os
from pathlib import Path
from dotenv import load_dotenv


# Устанавливаем корневую папку проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения из `.env`
load_dotenv(override=True)

# Секретный ключ приложения
SECRET_KEY = os.getenv("SECRET_KEY")

# Настройки API для отправки SMS
SMS_AERO_API_KEY = os.getenv("SMS_AERO_API_KEY")
SMS_AERO_SENDER = os.getenv("SMS_AERO_SENDER")

# Режим отладки (по умолчанию False)
DEBUG = os.getenv("DEBUG", "False") == "True"

# Разрешённые хосты (можно изменить в продакшене)
ALLOWED_HOSTS = ["*"]

# Указываем кастомную модель пользователя
AUTH_USER_MODEL = "users.User"

# Установленные приложения
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",  # Автодокументация API
    "users",  # Наше приложение пользователей
]

# Middleware (промежуточное ПО)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Основной файл маршрутов
ROOT_URLCONF = "config.urls"

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Настройки WSGI
WSGI_APPLICATION = "config.wsgi.application"

# Подключение базы данных PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("NAME"),
        "USER": os.getenv("USER"),
        "PASSWORD": os.getenv("PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT"),
    }
}

# Валидаторы паролей Django
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Локализация
LANGUAGE_CODE = "ru-RU"  # Установим русский язык

TIME_ZONE = "UTC"  # Часовой пояс (можно поменять на 'Europe/Moscow')

USE_I18N = True
USE_TZ = True

# Настройки статики
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

if DEBUG:
    # В режиме отладки файлы берутся из папки `static`
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    # В продакшене файлы собираются в `staticfiles/`
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Настройка поля по умолчанию для моделей Django
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URL-адрес для редиректа при попытке войти на защищённую страницу
LOGIN_URL = "/send-otp/"

# Настройка логирования (если понадобится)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/errors.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
