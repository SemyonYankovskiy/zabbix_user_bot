from aiogram.filters.callback_data import CallbackData


class AffectedSubscribersFactory(CallbackData, prefix="affected_subscribers"):
    from_minutes: int
