import logging
import sys
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from os import getenv
from fastapi import FastAPI



# Настройки веб-сервера
WEB_SERVER_HOST = "https://python-hello-world-uralnuthatchs-projects.vercel.app"
# Порты сервера: 
WEB_SERVER_PORT = 8350
# Путь к маршруту вебхука, по которому Telegram будет отправлять запросы
WEBHOOK_PATH = f''
# Базовый URL-адрес вебхука, который будет исп-ся для создания URL-адреса вебхука для Telegram
BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"
# На сервере только IPv6 (аналог ip4: 0.0.0.0).
WEBAPP_HOST = "0.0.0.0"


app = FastAPI()



@app.get("/")
async def setup():
    # Создаем объекты бота и диспетчера
    bot = Bot(token=getenv("BOT_TOKEN"), parse_mode='HTML')
    dp = Dispatcher()
    await bot.set_webhook(url=BASE_WEBHOOK_URL, drop_pending_updates=True)
    requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text=Hello')
    return "Webhook Updated"

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    #res = await dp.feed_webhook_update(bot, update)
    requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text=POST')
    #return res
