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
    async def on_startup(bot: Bot) -> None:
        await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")

    def main() -> None:
        # Создаем объекты бота и диспетчера
        bot = Bot(token=getenv("BOT_TOKEN"), parse_mode='HTML')
        dp = Dispatcher()

        # Этот хэндлер будет срабатывать на любые ваши текстовые сообщения
        # кроме команд "/start" и "/help"
        @dp.message()
        async def send_echo(message: Message):
            try:
                await message.send_copy(chat_id=message.chat.id)
            except TypeError:
                await message.reply(text = 'Данный тип апдейтов не поддерживается методом send_copy')

        # Register startup hook to initialize webhook
        dp.startup.register(on_startup)

        # Create aiohttp.web.Application instance
        app = web.Application()

        # Create an instance of request handler
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot
        )

        # Register webhook handler on application
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)

        # Mount dispatcher startup and shutdown hooks to aiohttp application
        setup_application(app, dp, bot=bot)

        # Запускаем веб-сервер
        web.run_app(app, host=WEBAPP_HOST)

    main()
    requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text=Hello')
    return "Webhook Updated"

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    #res = await dp.feed_webhook_update(bot, update)
    requests.get(f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage?chat_id=348123497&text=POST')
    #return res
