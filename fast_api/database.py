from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


MAX_NAME_LENGTH = 128
Base = declarative_base()


class User(Base):
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    tasks = relationship('Task', backref='auth_user')


class Tag(Base):
    __tablename__ = 'notebook_tag'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(MAX_NAME_LENGTH))
    slug = Column(String(MAX_NAME_LENGTH))

    tags = relationship('TaskTag', backref='notebook_tag')


class Task(Base):
    __tablename__ = 'notebook_task'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(MAX_NAME_LENGTH))
    description = Column(Text)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey('auth_user.id'))

    tasks = relationship('TaskTag', backref='notebook_task')
    comments = relationship('Comment', back_populates='task')

    class Config:
        ordering = ('completion_date',)


class TaskTag(Base):
    __tablename__ = 'notebook_tasktag'
    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey('notebook_tag.id'))
    task_id = Column(Integer, ForeignKey('notebook_task.id'))


class Comment(Base):
    __tablename__ = 'notebook_comment'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    task_id = Column(Integer, ForeignKey('notebook_task.id'))
    author_id = Column(Integer, ForeignKey('auth_user.id'))

    task = relationship('Task', back_populates='comments')
    author = relationship('User')

    class Config:
        ordering = ('-created_at',)
