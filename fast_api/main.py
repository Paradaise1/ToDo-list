import uvicorn
import os

from dotenv import load_dotenv
from typing import List

from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database import Base, User
from crud import (
    delete_comment,
    get_comment,
    get_comments,
    post_comment,
    put_comment,
    get_current_user_id
)
from shemas import CommentShema


load_dotenv()
app = FastAPI()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'django')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'django')
DATABASE_URL = (f'postgresql+asyncpg://'
                f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
                f'{DB_HOST}/{POSTGRES_DB}')

#DATABASE_URL = f'postgresql+asyncpg://postgres:rtyuehe777@localhost/test'


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session


@app.on_event('startup')
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/api/tasks/{task_id}/comments/{comment_id}/',
         response_model=CommentShema)
async def read_comments(
    task_id: int,
    comment_id: int,
    current_user_id: User = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    request_method = 'GET'
    comment = await get_comment(
        task_id, comment_id, current_user_id, request_method, db
    )
    return comment


@app.get('/api/tasks/{task_id}/comments/',
         response_model=List[CommentShema])
async def read_comments(
    task_id: int,
    current_user_id:
    User = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    comments = await get_comments(task_id, db)
    return comments


@app.post('/api/tasks/{task_id}/comments/',
          response_model=CommentShema)
async def create_comment(
    task_id: int,
    comment: CommentShema,
    current_user_id: User = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    db_comment = await post_comment(
        task_id, current_user_id, comment, db
    )
    return db_comment


@app.put('/api/tasks/{task_id}/comments/{comment_id}/',
         response_model=CommentShema)
async def modify_comment(
    task_id: int,
    comment: CommentShema,
    comment_id: int,
    current_user_id: User = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    request_method = 'PUT'
    db_comment = await put_comment(
        task_id, comment, comment_id, current_user_id, request_method, db
    )
    return db_comment


@app.delete('/api/tasks/{task_id}/comments/{comment_id}/')
async def deleting_comment(
    task_id: int,
    comment_id: int,
    current_user_id: User = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    request_method = 'DELETE'
    await delete_comment(
        task_id, comment_id, current_user_id, request_method, db
    )
    return


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080)
