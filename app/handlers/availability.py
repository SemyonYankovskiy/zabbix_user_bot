from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.service.check_users import get_affected_subscribers

from ..decorators.user_status import superuser_required
from ..callback_factories import AffectedSubscribersFactory
from ..text import WELCOME

router = Router()


def get_downs_keyboard(current_limit: int):
    limit_from_user = [
        ("Последние 30 минут", 30),
        ("Последний 1 час", 60),
        ("Последний 2 часа", 120),
        ("Последние 3 часа", 180),
    ]

    keyboard = []

    for name, minutes in limit_from_user:
        if current_limit == minutes:
            name = f"❇️{name}"
        callback_data = AffectedSubscribersFactory(from_minutes=minutes).pack()
        keyboard.append([InlineKeyboardButton(text=name, callback_data=callback_data)])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(Command("check_downs"))
@superuser_required
async def check_downs(message: types.Message):
    default_limit = 0
    keyboard = get_downs_keyboard(current_limit=default_limit)
    await message.answer(WELCOME, reply_markup=keyboard)


@router.callback_query(AffectedSubscribersFactory.filter())
@superuser_required
async def process_callback_button1(
    callback: types.CallbackQuery, callback_data: AffectedSubscribersFactory
):
    from_datetime = datetime.now() - timedelta(minutes=callback_data.from_minutes)
    data = await get_affected_subscribers(from_datetime=from_datetime)

    text = ""
    total_subscribers = 0
    for device, subscriber_count in data.items():
        if isinstance(subscriber_count, int):
            total_subscribers += subscriber_count
        text += f"{device}: {subscriber_count}\n"

    text += (
        f"\nОбщее кол-во оборудования: {len(data)}"
        f"\nОбщее кол-во абонентов: {total_subscribers}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_downs_keyboard(current_limit=callback_data.from_minutes),
    )
    await callback.answer()
