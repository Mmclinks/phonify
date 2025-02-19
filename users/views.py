from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import InviteCodeForm
from .models import User


def home(request):
    return render(request, "users/home.html")


@sync_to_async
def generate_otp(user, message):
    """Оборачиваем генерацию OTP в синхронную функцию."""
    user.generate_otp_code(message)


async def send_otp(request):
    """Отправка OTP-кода на номер телефона"""
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        user, created = await sync_to_async(User.objects.get_or_create)(
            phone_number=phone_number
        )
        # Асинхронная отправка OTP-кода
        await user.send_otp_code()
        messages.success(request, "OTP-код отправлен на ваш номер.")
        return redirect("verify_otp", phone_number=phone_number)
    return render(request, "users/send_otp.html")


def verify_otp(request, phone_number):
    """Проверка OTP-кода и завершение регистрации"""
    user = User.objects.filter(phone_number=phone_number).first()
    if not user:
        messages.error(request, "Пользователь с таким номером не найден.")
        return redirect("send_otp")
    if request.method == "POST":
        otp_code = request.POST.get("otp_code")
        if user.otp_code == otp_code:
            login(request, user)  # Авторизация пользователя
            if not user.invite_code:
                user.generate_invite_code()  # Генерация инвайт-кода, если его нет
                user.save()  # Сохраняем инвайт-код
            return redirect("profile")  # Переход в профиль пользователя
        else:
            messages.error(request, "Неверный код.")
    return render(request, "users/verify_otp.html", {"phone_number": phone_number})


@login_required
def enter_invite_code(request):
    """Ввод инвайт-кода для получения реферала"""
    if request.method == "POST":
        form = InviteCodeForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data["invite_code"]
            try:
                # Ищем пользователя по инвайт-коду
                inviter = User.objects.get(invite_code=invite_code)
                current_user = request.user
                if current_user.invited_by:
                    messages.error(request, "Вы уже использовали инвайт-код.")
                else:
                    current_user.invited_by = (
                        inviter  # Связываем пользователя с тем, кто его пригласил
                    )
                    current_user.save()
                    messages.success(request, "Инвайт-код принят!")
                return redirect("profile")
            except User.DoesNotExist:
                messages.error(request, "Неверный инвайт-код.")
    else:
        form = InviteCodeForm()
    return render(request, "users/enter_invite_code.html", {"form": form})


@login_required
def profile(request):
    """Профиль пользователя с информацией о приглашениях и инвайт-кодах"""
    return render(request, "users/profile.html", {"user": request.user})
