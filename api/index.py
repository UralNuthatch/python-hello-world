import logging
import sys
import requests
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from os import getenv
from fastapi import FastAPI
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))

        # Настройки веб-сервера
        WEB_SERVER_HOST = "https://python-hello-world-uralnuthatchs-projects.vercel.app"
        # Порты сервера: 
        WEB_SERVER_PORT = 8350
        # Путь к маршруту вебхука, по которому Telegram будет отправлять запросы
        WEBHOOK_PATH = f'/bot/{getenv("BOT_TOKEN")}'
        # Базовый URL-адрес вебхука, который будет исп-ся для создания URL-адреса вебхука для Telegram
        BASE_WEBHOOK_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"
        # На сервере только IPv6 (аналог ip4: 0.0.0.0).
        WEBAPP_HOST = "0.0.0.0"

        # Создаем объекты бота и диспетчера
        bot = Bot(token=getenv("BOT_TOKEN"))
        dp = Dispatcher()

        async def setup():
            await bot.set_webhook(url=BASE_WEBHOOK_URL, drop_pending_updates=True)

        asyncio.run(setup())

        
        
        return
