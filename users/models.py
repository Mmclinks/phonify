"""
Модели и методы для работы с пользователями в системе Phonify.

Модуль содержит модель пользователя `User`, которая расширяет стандартную модель
Django `AbstractUser`, а также методы для:
- Генерации и отправки OTP-кода для аутентификации.
- Генерации уникального инвайт-кода для пользователя.
"""

import random
import string

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.sms import send_sms_via_smsAero


class User(AbstractUser):
    """
    Модель пользователя Phonify.

    Поля:
    - username: имя пользователя, необязательное.
    - phone_number: номер телефона (уникальный).
    - invite_code: инвайт-код (уникальный, необязательный).
    - invited_by: пользователь, который пригласил текущего (если есть).
    - otp_code: код подтверждения для аутентификации.
    - otp_sent_at: время отправки OTP-кода.

    Требования:
    - PHONE_NUMBER используется как поле для входа в систему (USERNAME_FIELD).
    - `REQUIRED_FIELDS` включает `username`, которое обязательно для миграций.
    """

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    invited_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invitees",
    )
    otp_code = models.CharField(max_length=4, null=True, blank=True)
    otp_sent_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    @sync_to_async
    def generate_otp_code(self):
        """
        Генерация случайного 4-значного OTP-кода.

        Сохраняет OTP-код в базе данных и возвращает его.

        :return: OTP-код как строку.
        """
        otp_code = str(random.randint(1000, 9999))
        self.otp_code = otp_code
        self.save()
        return otp_code

    async def send_otp_code(self):
        """
        Асинхронная отправка OTP-кода на номер телефона через SMS.

        Генерирует OTP-код и отправляет его пользователю на телефон.
        Использует внешнюю утилиту для отправки SMS через SMSAero.

        :return: None
        """
        otp_code = await self.generate_otp_code()  # Оборачиваем в sync_to_async
        message = f"Ваш код для авторизации: {otp_code}"
        await send_sms_via_smsAero(self.phone_number, message)

    def generate_invite_code(self):
        """
        Генерация уникального инвайт-кода.

        Генерирует случайный инвайт-код, проверяет его на уникальность,
        сохраняет в базе данных и присваивает пользователю.

        :return: None
        """
        chars = string.ascii_letters + string.digits
        while True:
            code = "".join(random.choices(chars, k=6))
            if not User.objects.filter(invite_code=code).exists():
                self.invite_code = code
                self.save()
                break
