from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User, Subscription
from app.security.services import get_current_user
from app.users.schemas import UserSubscribeSchema
from app.users.services import get_user_by_username

subs_router = APIRouter()


@subs_router.post("/subscribe/{username}")
async def subscribe_user(
    username: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    подписка на пользователя
    user: текущий пользователь
    если пользователь не найден - ошибка 404
    возвращает искомого пользователя (на которого хотим подписаться)
    """

    # запрос в базу данных для поиска пользователя по юзернейму
    target_user = await get_user_by_username(session, username)

    if not target_user:
        raise HTTPException(status_code=404, detail="user not found")

    # проверяем, подписан ли user (текущий) на target_user (искомый)
    existing_subscription = await session.execute(
        select(Subscription).where(
            Subscription.subscriber_id == user.id,
            Subscription.subscribed_to_id == target_user.id,
        )
    )
    existing_subscription = existing_subscription.scalar_one_or_none()

    if existing_subscription:
        raise HTTPException(status_code=400, detail="you have already subscribed")

    # подписываемся
    new_subscription = Subscription(
        subscriber_id=user.id, subscribed_to_id=target_user.id
    )

    # добавляем запись в базу данных и сохраняем
    session.add(new_subscription)
    await session.commit()

    return target_user


@subs_router.post("/unsubscribe/{username}")
async def unsubscribe_user(
    username: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    отписка от пользователя
    user: текущий пользователь
    если пользователь не найден - ошибка 404
    возвращает искомого пользователя (от которого хотим отписаться)
    """

    target_user = await get_user_by_username(session, username)

    if not target_user:
        raise HTTPException(status_code=404, detail="user not found")

    # проверяем подписан ли user на target_user
    subscription = await session.execute(
        select(Subscription).where(
            Subscription.subscriber_id == user.id,
            Subscription.subscribed_to_id == target_user.id,
        )
    )
    subscription = subscription.scalar_one_or_none()
    # если не подписан
    if not subscription:
        raise HTTPException(status_code=400, detail="you are not subscribed")

    # если подписка есть, удаляем из базы данных и сохраняем
    await session.delete(subscription)
    await session.commit()

    return target_user


@subs_router.get("/subscriptions")
async def get_subscriptions(
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
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


@subs_router.get("/subscribers")
async def get_subscribers(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
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
