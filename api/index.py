import logging
import sys
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, Update
from aiogram.filters import Command, CommandStart
from os import getenv
from fastapi import FastAPI
from contextlib import asynccontextmanager


# Настройки веб-сервера
WEB_SERVER_HOST = "https://python-hello-world-zeta-khaki.vercel.app"
# Порты сервера: 
WEB_SERVER_PORT = 8350
# Путь к маршруту вебхука, по которому Telegram будет отправлять запросы
WEBHOOK_PATH = f'/bot/{getenv("BOT_TOKEN")}'
# Базовый URL-адрес вебхука, который будет исп-ся для создания URL-адреса вебхука для Telegram
BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"
# На сервере только IPv6 (аналог ip4: 0.0.0.0).
WEBAPP_HOST = "0.0.0.0"

@asynccontextmanager
async def lifespan(app: FastAPI):
#webhook_info = await bot.get_webhook_info()
#if webhook_info.url != BASE_WEBHOOK_URL:
    await bot.set_webhook(url=BASE_WEBHOOK_URL)
    yield
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

# Создаем объекты бота и диспетчера
bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text = 'Данный тип апдейтов не поддерживается методом send_copy')

@app.get("/")
async def setup():
#    await bot.set_webhook(url=BASE_WEBHOOK_URL, drop_pending_updates=True)
#    requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text=Hello')
    return "Webhook Updated"

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    #await dp.feed_webhook_update(bot, update)
    task = asyncio.create_task(dp.feed_webhook_update(bot, update))
    await task
    requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text={update}')
