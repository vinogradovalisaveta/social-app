from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import Depends

from security.services import get_current_user
from users.models import User
from subscription.models import Subscription
from users.schemas import UserSubscribeSchema


async def get_follows(
    user: User = Depends(), session: AsyncSession = Depends()
) -> list:
    """
    получение списка подписок
    user: текущий пользователь
    возвращает список юзернеймов подписок
    """

    # запрос в базу данных, где ищем текущего пользователя и его подписки
    query = (
        select(User)
        .join(Subscription, and_(User.id == Subscription.subscribed_to_id))
        .where(Subscription.subscriber_id == user.id)
    )

    result = await session.execute(query)
    result = result.scalars().all()

    return [UserSubscribeSchema(username=user.username) for user in result]


async def get_followers(
    user: User = Depends(),
    session: AsyncSession = Depends(),
):
    """
    получение списка подписчиков
    user: текущий пользователь
    возвращает список юзернеймов подписчиков
    """

    # запрос в базу данных, где находим текущего пользователя и его подписчиков
    query = (
        select(User)
        .join(Subscription, and_(User.id == Subscription.subscriber_id))
        .where(Subscription.subscribed_to_id == user.id)
    )

    result = await session.execute(query)
    result = result.scalars().all()

    return [UserSubscribeSchema(username=user.username) for user in result]
