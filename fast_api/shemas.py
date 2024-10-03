from pydantic import BaseModel
from datetime import datetime


class CommentShema(BaseModel):
    content: str

# class CommentCreate(CommentShema):
#     id: int
#     created_at: datetime
#     author_id: int
#     task_id: int

#     class Config:
#         orm_mode = True
