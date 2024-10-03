import json
import jwt
import os

from dotenv import load_dotenv
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis import Redis
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Comment
from shemas import CommentShema


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

# redis_client = Redis(host='localhost', port=6379, db=0)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    return decode_jwt_token(token)


async def get_item(
        task_id: int,
        item_id: int,
        author_id: int,
        request_method: str,
        db: AsyncSession
):
    # cached_data = redis_client.get(f'comment:{task_id}:{item_id}')
    # if cached_data and request_method == 'GET':
    #     content = json.loads(cached_data)
    #     return {'content': str(content)}
    item = await db.execute(select(Comment).where(
        Comment.id == item_id, Comment.task_id == task_id))
    comment = item.scalars().first()
    # redis_client.set(f'comment:{task_id}:{item_id}', comment.content)
    if comment:
        return comment
    raise HTTPException(status_code=400)


async def get_comments(task_id: int, db: AsyncSession):
    comments = await db.execute(
        select(Comment).where(Comment.task_id == task_id)
    )
    comments = comments.scalars().all()
    return comments


async def get_comment(
        task_id: int,
        comment_id: int,
        author_id: int,
        request_method: str,
        db: AsyncSession
):
    return await get_item(task_id, comment_id, author_id, request_method, db)


async def post_comment(
        task_id: int,
        author_id: int,
        comment: CommentShema,
        db: AsyncSession
):
    db_comment = Comment(
        content=comment.content, task_id=task_id, author_id=author_id
    )
    db.add(db_comment)
    await db.flush()
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def put_comment(
        task_id: int,
        comment: CommentShema,
        comment_id: int,
        author_id: int,
        request_method: str,
        db: AsyncSession
):
    db_comment = await get_item(
        task_id, comment_id, author_id, request_method, db
    )
    if db_comment:
        db_comment.content = comment.content
        await db.flush()
        await db.commit()
        await db.refresh(db_comment)
    return db_comment


async def delete_comment(
        task_id: int,
        comment_id: int,
        author_id: int,
        request_method: str,
        db: AsyncSession
):
    db_comment = await get_item(
        task_id, comment_id, author_id, request_method, db
    )
    if db_comment:
        await db.flush()
        await db.delete(db_comment)
        await db.commit()
    return
