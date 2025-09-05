import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

if os.environ.get("PROXY"):
    session = AiohttpSession(proxy=os.environ.get("PROXY"))
else:
    session = AiohttpSession()

bot = Bot(token="6326983114:AAFvRIdFH9zGBcn4oQVmKEqfJmRnzuqgk1g", session=session)
dp = Dispatcher(storage=MemoryStorage())
