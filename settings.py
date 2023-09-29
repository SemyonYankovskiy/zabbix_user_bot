import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

bot = Bot(token="")
dp = Dispatcher(storage=MemoryStorage())
