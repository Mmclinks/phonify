"""
Формы для работы с регистрацией и инвайт-кодами в приложении пользователей.

Этот модуль содержит формы на основе Django Forms и ModelForm для валидации
и обработки данных, вводимых пользователями.
"""

from django import forms

from .models import User


class RegisterForm(forms.ModelForm):
    """
    Форма регистрации пользователя.

    Поля:
    - otp_code: код подтверждения (4 символа, обязательное поле).
    - username: имя пользователя (берется из модели User).
    - phone_number: номер телефона (берется из модели User).

    Валидация:
    - Проверяет, что номер телефона введен (не пустое значение).
    """

    otp_code = forms.CharField(max_length=4, required=True, label="Код подтверждения")

    class Meta:
        model = User
        fields = ["username", "phone_number"]

    def clean_phone_number(self):
        """
        Проверяет, что номер телефона не пустой.

        :return: очищенный номер телефона
        :raises forms.ValidationError: если поле пустое
        """
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            raise forms.ValidationError("Номер телефона обязателен.")
        return phone_number


class InviteCodeForm(forms.Form):
    """
    Форма для ввода инвайт-кода.

    Поля:
    - invite_code: 6-значный код, обязательное поле.
    """

    invite_code = forms.CharField(max_length=6, required=True, label="Инвайт-код")
