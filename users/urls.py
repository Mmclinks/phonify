from django.urls import path
from .views import home, verify_otp, enter_invite_code, profile, send_otp

urlpatterns = [
    path('', home, name='home'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/<str:phone_number>/', verify_otp, name='verify_otp'),
    path('enter-invite/', enter_invite_code, name='enter_invite_code'),
    path('profile/', profile, name='profile'),
]
