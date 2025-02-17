from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'invite_code', 'invited_by']


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        user, created = User.objects.get_or_create(phone_number=phone_number)
        user.generate_otp_code()
        return user


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_code = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp_code = data.get('otp_code')
        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.otp_code == otp_code:
            return user
        raise serializers.ValidationError("Неверный код.")
