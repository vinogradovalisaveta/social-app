from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.suite.test_reflection import users

from app.database import get_session
from app.models import User, Subscription
from app.security.services import get_current_user
from app.users.schemas import UserSubscribeSchema

subs_router = APIRouter()


@subs_router.post("/subscribe/{username}")
async def subscribe_user(
    username: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    # search for user to subscribe
    target_user = await session.execute(select(User).where(User.username == username))
    target_user = target_user.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="user not found")

    # check if user is already subscribed
    existing_subscription = await session.execute(
        select(Subscription).where(
            Subscription.subscriber_id == user.id,
            Subscription.subscribed_to_id == target_user.id,
        )
    )
    existing_subscription = existing_subscription.scalar_one_or_none()

    if existing_subscription:
        raise HTTPException(status_code=400, detail="you have already subscribed")

    # subscribing
    new_subscription = Subscription(
        subscriber_id=user.id, subscribed_to_id=target_user.id
    )
    session.add(new_subscription)
    await session.commit()

    return target_user


@subs_router.post("/unsubscribe/{username}")
async def unsubscribe_user(
    username: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    target_user = await session.execute(select(User).where(User.username == username))
    target_user = target_user.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="user not found")

    subscription = await session.execute(
        select(Subscription).where(
            Subscription.subscriber_id == user.id,
            Subscription.subscribed_to_id == target_user.id,
        )
    )
    subscription = subscription.scalar_one_or_none()

    if not subscription:
        raise HTTPException(status_code=400, detail="you are not subscribed")

    await session.delete(subscription)
    await session.commit()

    return target_user


@subs_router.get("/subscriptions")
async def get_subscriptions(
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
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
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    query = (
        select(User)
        .join(Subscription, and_(User.id == Subscription.subscriber_id))
        .where(Subscription.subscribed_to_id == user.id)
    )
    result = await session.execute(query)
    result = result.scalars().all()
    return [UserSubscribeSchema(username=user.username) for user in result]
