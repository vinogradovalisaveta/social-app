from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from comments.schemas import CommentAddSchema, CommentReadSchema
from security.services import get_current_user
from database import get_session
from users.models import User
from sqlalchemy import select
from comments.models import Comment
from posts.services import read_post

router = APIRouter(tags=["comments"])


@router.delete("/{post.slug}/comments")
async def delete_comment(
    comment_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    comment = (
        await session.execute(select(Comment).where(Comment.id == comment_id))
    ).scalar_one_or_none()
    if comment is None:
        raise HTTPException(status_code=404, detail="comment not found")

    if comment.author_username != user.username:
        raise HTTPException(status_code=403, detail="forbidden")

    await session.delete(comment)
    await session.commit()
    return comment


@router.post("/{post.slug}/comments")
async def add_comment(
    comment: CommentAddSchema,
    slug: str,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    post = await read_post(session, slug)

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    comment = Comment(
        post_slug=post.slug,
        author_username=user.username,
        text=comment.text,
    )

    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return CommentReadSchema(
        author_username=comment.author_username,
        text=comment.text,
        created_at=comment.created_at,
    )


@router.get("/{post.slug}/comments", response_model=List[CommentReadSchema])
async def get_comments_to_post(
    slug: str,
    session: AsyncSession = Depends(get_session),
):

    comments = (
        (await session.execute(select(Comment).where(Comment.post_slug == slug)))
        .scalars()
        .all()
    )

    return comments


@router.post("/{post.slug}/{comment.id}/replies")
async def add_reply_to_comment(
    comment_id: int,
    reply: CommentAddSchema,
    author: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    comment = (
        await session.execute(select(Comment).where(Comment.id == comment_id))
    ).scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")

    new_reply = Comment(
        post_slug=comment.post_slug,
        author_username=author.username,
        text=reply.text,
        parent_id=comment.id,
    )

    session.add(new_reply)
    await session.commit()
    await session.refresh(new_reply)
    return new_reply
