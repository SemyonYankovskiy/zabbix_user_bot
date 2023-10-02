from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.service.check_users import AffectedSubscribersChecker

from ..decorators.user_status import superuser_required
from ..text import WELCOME

router = Router()


# async def get_downs_keyboard():
#     builder = InlineKeyboardBuilder()
#     builder.row(
#         types.InlineKeyboardButton(text="Последние 30 минут",callback_data="min30",),
#         types.InlineKeyboardButton(text="Последние 60 минут",callback_data="min60",),)
#     builder.row(
#         types.InlineKeyboardButton(text="Последний 2 час", callback_data="min120"),
#         types.InlineKeyboardButton(text="Последние 3 часа", callback_data="min180"),)
#     return builder.as_markup()
#
#
# @router.message(Command("check_downs"))
# @superuser_required
# async def check_downs(message: types.Message):
#     default_limit = "min:30"
#     keyboard = await get_downs_keyboard()
#     await message.answer(WELCOME, reply_markup=keyboard)
#
#
# @router.callback_query(F.data == "min30")
# async def min30(callback: types.CallbackQuery):
#     result = AffectedSubscribersChecker().get_affected_subscribers()
#     keyboard = await get_downs_keyboard()
#     await callback.answer(reply_markup=keyboard)
#     print(result)
#     print(str(result))
#     await callback.message.answer(str(result))
############################################################################


def get_downs_keyboard(current_limit: str):
    limit_from_user = [
        ("Последние 30 минут", "min:30"),
        ("Последний 1 час", "min:60"),
        ("Последний 2 часа", "min:120"),
        ("Последние 3 часа", "min:180"),
    ]

    keyboard = []

    for name, callback_data in limit_from_user:
        if current_limit == callback_data:
            name = f"❇️ {name}"
        keyboard.append([InlineKeyboardButton(text=name, callback_data=callback_data)])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(Command("check_downs"))
@superuser_required
async def check_downs(message: types.Message):
    default_limit = "min:30"
    keyboard = get_downs_keyboard(current_limit=default_limit)
    await message.answer(WELCOME, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "min:30" or c.data == "min:60" or c.data == "min:120" or c.data == "min:180")
async def process_callback_button1(callback: types.CallbackQuery):
    limit_str = callback.data[4:]
    print(limit_str)
    time_limit = callback.data
    result = AffectedSubscribersChecker().get_affected_subscribers()

    await callback.message.answer(str(result))
    await callback.message.answer(limit_str)
