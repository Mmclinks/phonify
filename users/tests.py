import pytest
from django.contrib.messages.middleware import MessageMiddleware
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from .models import User
from .forms import InviteCodeForm
from .views import home, send_otp, verify_otp, enter_invite_code, profile

@pytest.mark.django_db
def test_home_view():
    factory = RequestFactory()
    request = factory.get('/')
    response = home(request)
    assert response.status_code == 200


from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from asgiref.sync import sync_to_async


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_send_otp_view():
    factory = RequestFactory()
    request = factory.post('/send_otp/', {'phone_number': '1234567890'})
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)

    # Оборачиваем сохранение сессии в sync_to_async
    await sync_to_async(request.session.save)()

@pytest.mark.django_db
def test_verify_otp_view():
    user = User.objects.create(phone_number='1234567890', otp_code='1234')
    factory = RequestFactory()
    request = factory.post('/verify_otp/1234567890/', {'otp_code': '1234'})
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    response = verify_otp(request, '1234567890')
    assert response.status_code == 302
    assert response.url == reverse('profile')


@pytest.mark.django_db
def test_enter_invite_code_view():
    user = User.objects.create(phone_number='1234567890', invite_code='ABCDEF')

    # Создаем запрос
    factory = RequestFactory()
    request = factory.post('/enter_invite_code/', {'invite_code': 'ABCDEF'})

    # Добавляем необходимые middleware
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)

    # Добавляем MessageMiddleware
    message_middleware = MessageMiddleware(lambda req: None)
    message_middleware.process_request(request)

    # Устанавливаем пользователя
    request.user = user

    # Вызываем представление
    response = enter_invite_code(request)

    # Проверка редиректа
    assert response.status_code == 302
    assert response.url == '/profile/'  # Если редирект на страницу профиля


@pytest.mark.django_db
def test_profile_view():
    user = User.objects.create(phone_number='1234567890')
    factory = RequestFactory()
    request = factory.get('/profile/')
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.user = user
    response = profile(request)
    assert response.status_code == 200
