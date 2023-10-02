from hmac import compare_digest

from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from app.models import User


router = Router()


@router.message(Command("become"))
async def become_admin(message: types.Message):
    _, token = message.text.split()
    user = await User.get_or_create(message.from_user)

    if user.is_superuser:
        await message.answer("Вы уже суперпользователь")
    elif compare_digest(token, "cus"):
        user.is_superuser = True
        await user.update(is_superuser=True)
        await message.answer("Вы стали суперпользователем")
    else:
        await message.answer("Нет доступа")
