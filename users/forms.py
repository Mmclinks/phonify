
from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    otp_code = forms.CharField(max_length=4, required=True, label="Код подтверждения")

    class Meta:
        model = User
        fields = ['username', 'phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError("Номер телефона обязателен.")
        return phone_number


class InviteCodeForm(forms.Form):
    invite_code = forms.CharField(max_length=6, required=True, label="Инвайт-код")

