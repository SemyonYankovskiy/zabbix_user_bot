from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.service.check_users import AffectedSubscribersChecker

from ..decorators.user_status import superuser_required
from ..models import User
from ..text import WELCOME
from datetime import datetime

router = Router()






async def get_downs_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Последние 30 минут",callback_data="min30",),
        types.InlineKeyboardButton(text="Последние 60 минут",callback_data="min60",),)
    builder.row(
        types.InlineKeyboardButton(text="Последний 2 час", callback_data="min120"),
        types.InlineKeyboardButton(text="Последние 3 часа", callback_data="min180"),)

    return builder.as_markup()


@router.message(Command("check_downs"))
@superuser_required
async def check_downs(message: types.Message):
    print("check_downs")
    await message.answer("Ты суперпользователь")
    keyboard = await get_downs_keyboard()
    await message.answer(WELCOME, reply_markup=keyboard)



@router.callback_query(F.data == "min30")
async def min30(callback: types.CallbackQuery):
    result = AffectedSubscribersChecker().get_affected_subscribers()
    keyboard = await get_downs_keyboard()
    await callback.answer(reply_markup=keyboard)
    print(result)
    print(str(result))
    await callback.message.answer(str(result))

