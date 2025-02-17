import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from asgiref.sync import sync_to_async
from utils.sms import send_sms_via_smsAero


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    invited_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='invitees')
    otp_code = models.CharField(max_length=4, null=True, blank=True)
    otp_sent_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    @sync_to_async
    def generate_otp_code(self):
        """Генерация и сохранение OTP-кода (вызов синхронной ORM-операции через sync_to_async)"""
        otp_code = str(random.randint(1000, 9999))
        self.otp_code = otp_code
        self.save()
        return otp_code

    async def send_otp_code(self):
        """Асинхронная отправка OTP-кода через SMS"""
        otp_code = await self.generate_otp_code()  # Оборачиваем в sync_to_async
        message = f"Ваш код для авторизации: {otp_code}"
        await send_sms_via_smsAero(self.phone_number, message)
    def generate_invite_code(self):
        """Генерация уникального инвайт-кода"""
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(chars, k=6))
            if not User.objects.filter(invite_code=code).exists():
                self.invite_code = code
                self.save()
                break
