"""
Сериализаторы для работы с пользователями и валидации OTP-кодов.

Модуль содержит сериализаторы для:
- Сериализации данных пользователя (`UserSerializer`).
- Генерации и валидации OTP-кодов для авторизации пользователя (`OTPSerializer`, `VerifyOTPSerializer`).
"""

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.

    Используется для представления данных пользователя, таких как:
    - username: имя пользователя.
    - phone_number: номер телефона.
    - invite_code: инвайт-код пользователя.
    - invited_by: пользователь, который пригласил текущего.
    """

    class Meta:
        model = User
        fields = ["username", "phone_number", "invite_code", "invited_by"]


class OTPSerializer(serializers.Serializer):
    """
    Сериализатор для генерации OTP-кода.

    Включает поле:
    - phone_number: номер телефона пользователя, для которого нужно сгенерировать OTP.

    Валидация:
    - Если пользователь с таким номером не существует, он создается, а затем генерируется OTP-код.
    """

    phone_number = serializers.CharField()

    def validate(self, data):
        """
        Валидация и генерация OTP-кода.

        :param data: данные сериализатора, включающие номер телефона.
        :return: пользователь, для которого сгенерирован OTP-код.
        :raises serializers.ValidationError: если пользователь не может быть создан.
        """
        phone_number = data.get("phone_number")
        user, created = User.objects.get_or_create(phone_number=phone_number)
        user.generate_otp_code()
        return user


class VerifyOTPSerializer(serializers.Serializer):
    """
    Сериализатор для проверки OTP-кода.

    Включает поля:
    - phone_number: номер телефона пользователя, для которого нужно проверить OTP.
    - otp_code: OTP-код, введенный пользователем.

    Валидация:
    - Проверяет, совпадает ли OTP-код с сохраненным кодом для данного пользователя.
    """

    phone_number = serializers.CharField()
    otp_code = serializers.CharField()

    def validate(self, data):
        """
        Валидация OTP-кода.

        :param data: данные сериализатора, включающие номер телефона и OTP-код.
        :return: пользователь, если OTP-код правильный.
        :raises serializers.ValidationError: если OTP-код неверный.
        """
        phone_number = data.get("phone_number")
        otp_code = data.get("otp_code")
        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.otp_code == otp_code:
            return user
        raise serializers.ValidationError("Неверный код.")
