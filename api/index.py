import logging
import requests
import asyncio
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

# включение логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: "
            "%(filename)s: "
            "%(levelname)s: "
            "%(funcName)s(): "
            "%(lineno)d:\t"
            "%(message)s",
)
logging.info("Application started")


async def setup_app():
    app = FastAPI()

    # Создаем объекты бота и диспетчера
    bot = Bot(token=getenv("BOT_TOKEN"), parse_mode='HTML')
    dp = Dispatcher()

    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(Command(commands=["start"]))
    async def process_start_command(message: Message):
        await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

    # Этот хэндлер будет срабатывать на команду "/help"
    @dp.message(Command(commands=['help']))
    async def process_help_command(message: Message):
        await message.answer('Напиши мне что-нибудь и в ответ\nя пришлю тебе твое сообщение')

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
        await bot.set_webhook(url=BASE_WEBHOOK_URL, drop_pending_updates=True)
        requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text=Hello')
        return "Webhook Updated"

    @app.post(WEBHOOK_PATH)
    async def bot_webhook(update: dict):
        res = await dp.feed_webhook_update(bot, update)
        requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text=POST')
        return res

    return app

app = asyncio.run(setup_app())
