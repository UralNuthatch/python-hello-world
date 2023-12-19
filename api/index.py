import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from os import getenv

from aiohttp import web

from http.server import BaseHTTPRequestHandler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))
        return


# Настройки веб-сервера
WEB_SERVER_HOST = "http://python-hello-world-uralnuthatchs-projects.vercel.app/"
# Порты сервера: 8300-8499
WEB_SERVER_PORT = "8350"
# Путь к маршруту вебхука, по которому Telegram будет отправлять запросы
WEBHOOK_PATH = ""
# Базовый URL-адрес вебхука, который будет исп-ся для создания URL-адреса вебхука для Telegram
BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"
# На сервере только IPv6 (аналог ip4: 0.0.0.0)
WEBAPP_HOST = "::"


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")

def main() -> None:

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


if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
