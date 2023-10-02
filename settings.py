import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

bot = Bot(token="6326983114:AAFvRIdFH9zGBcn4oQVmKEqfJmRnzuqgk1g")
dp = Dispatcher(storage=MemoryStorage())
