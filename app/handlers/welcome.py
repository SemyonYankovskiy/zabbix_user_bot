from aiogram import Router, types
from aiogram.filters import Command
from ..models import User

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = await User.get_or_create(tg_user=message.from_user)
    await message.answer(f"Привет, {message.from_user.username}, работаем")
    if user.is_superuser:
        await message.answer("Вы суперпользователь")
    else:
        await message.answer("Нет доступа\nОбратитесь к администратору")
