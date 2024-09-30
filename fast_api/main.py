import sqlite3
import json

from datetime import date, datetime

from fastapi import FastAPI, HTTPException
from redis import Redis
from pydantic import BaseModel, field_validator


app = FastAPI()

redis_client = Redis(host='localhost', port=6379, db=0)

DATABASE = 'db.sqlite3'


class CommentCreate(BaseModel):
    content: str
    created_at: date
    task_id: int
    author_id: int

    @field_validator('created_at', pre=True)
    def string_to_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%d-%b-%Y').date()
        return v


class CommentResponse(CommentCreate):
    id: int


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.get('api/tasks/{task_id}/comments/{comment_id}', response_model=CommentResponse)
async def get_comment(comment: CommentCreate, comment_id: int):
    cached_comment = redis_client.get(f'comment:{comment_id}')
    
    if cached_comment:
        return json.loads(cached_comment)
    
    if comment_id == comment['id']:
        redis_client.set(f'comment:{comment_id}', json.dumps(comment))
        return comment
    
    raise HTTPException(status_code=404, detail='Comment not found')


@app.post('api/tasks/{task_id}/comments/', response_model=CommentResponse)
async def create_comment(comment: CommentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todo_list_comment '
                   '(content, created_at, task_id, author_id) '
                   'VALUES (?, ?, ?, ?)', 
                   (comment.title,
                    comment.created_at,
                    comment.task_id,
                    comment.author_id))
    conn.commit()
    conn.close()
    return comment


# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from pydantic import BaseModel

# # FastAPI app instance
# app = FastAPI()

# # Database setup
# DATABASE_URL = &quot;sqlite:///./test.db&quot;
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# # Database model
# class Item(Base):
#     __tablename__ = &quot;items&quot;
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)


# # Create tables
# Base.metadata.create_all(bind=engine)


# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Pydantic model for request data
# class ItemCreate(BaseModel):
#     name: str
#     description: str


# # Pydantic model for response data
# class ItemResponse(BaseModel):
#     id: int
#     name: str
#     description: str


# # API endpoint to create an item
# @app.post(&quot;/items/&quot;, response_model=ItemResponse)
# async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
#     db_item = Item(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


# # API endpoint to read an item by ID
# @app.get(&quot;/items/{item_id}&quot;, response_model=ItemResponse)
# async def read_item(item_id: int, db: Session = Depends(get_db)):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if db_item is None:
#         raise HTTPException(status_code=404, detail=&quot;Item not found&quot;)
#     return db_item
