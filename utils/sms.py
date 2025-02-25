import os

import aiohttp
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

SMSAERO_EMAIL = os.getenv("SMSAERO_EMAIL")
SMSAERO_API_KEY = os.getenv("SMSAERO_API_KEY")


async def send_sms_via_smsAero(phone_number, message):
    """Функция для отправки SMS через smsaero.ru (асинхронная версия)"""
    email = SMSAERO_EMAIL  # Используем загруженные ранее переменные
    api_key = SMSAERO_API_KEY

    if not email or not api_key:
        raise ValueError("API credentials are missing.")

    url = f"https://gate.smsaero.ru/v2/sms/send?number={phone_number}&text={message}&sign=SMS Aero"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, auth=aiohttp.BasicAuth(email, api_key)) as response:
            return await response.json()
