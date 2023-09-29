from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    update as sqlalchemy_update,
)
from aiogram.types import User as TGUser

from database.base import Base
from database.connection import db
from database.manager import Manager


class User(Base, Manager):
    __tablename__ = "users"

    tg_id = Column(Integer(), primary_key=True, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    is_superuser = Column(Boolean(), nullable=False, default=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    date_joined = Column(DateTime(), nullable=False)
    is_active = Column(Boolean(), nullable=False, default=True)

    def __str__(self):
        return f"User: TG:{self.tg_id} ({self.username})"

    @classmethod
    async def exist(cls, tg_id: int) -> bool:
        try:
            await cls.get(tg_id=tg_id)
            return True
        except cls.DoesNotExists:
            return False

    @classmethod
    async def get_or_create(cls, tg_user: TGUser) -> "User":
        try:
            return await cls.get(tg_id=tg_user.id)
        except cls.DoesNotExists:
            return await cls.create(
                tg_id=tg_user.id,
                username=tg_user.username or str(tg_user.id),
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                date_joined=datetime.now(),
            )

    async def update(self, **kwargs) -> None:
        """
        # Обновляет текущий объект.
        :param kwargs: Поля и значения, которые надо поменять.
        """

        async with db.session() as session:
            await session.execute(
                sqlalchemy_update(self.__class__), [{"tg_id": self.tg_id, **kwargs}]
            )
            await session.commit()
