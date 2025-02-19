from django.urls import path

from .views import enter_invite_code, home, profile, send_otp, verify_otp

urlpatterns = [
    path("", home, name="home"),
    # Главная страница
    # Отображает основную страницу приложения, используемую как точку входа в приложение.
    path("send-otp/", send_otp, name="send_otp"),
    # Отправка OTP-кода
    # Эндпоинт для отправки OTP-кода на номер телефона пользователя. Ожидает номер телефона для отправки кода.
    path("verify-otp/<str:phone_number>/", verify_otp, name="verify_otp"),
    # Проверка OTP-кода
    # Этот эндпоинт проверяет OTP-код, отправленный пользователю. Требуется номер телефона и OTP-код.
    # Если код верный, пользователь авторизуется.
    path("enter-invite/", enter_invite_code, name="enter_invite_code"),
    # Ввод инвайт-кода
    # Эндпоинт для ввода инвайт-кода. Используется пользователями для ввода полученного инвайт-кода.
    path("profile/", profile, name="profile"),
    # Профиль пользователя
    # Этот эндпоинт позволяет пользователю просматривать и редактировать свой профиль,
    # включая имя, телефон и инвайт-код.
]
