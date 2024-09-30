from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_NAME_LENGTH, TEXT_LIMIT


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_NAME_LENGTH, verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name[:TEXT_LIMIT]}'


class Task(models.Model):
    title = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    completed = models.BooleanField(default=False, verbose_name='Завершено')
    completion_date = models.DateTimeField(verbose_name='Дата исполнения')
    author = models.ForeignKey(
        User, related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag, through='TaskTag', verbose_name='Тэг'
    )

    class Meta:
        ordering = ('completion_date',)
        verbose_name = 'задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.title[:TEXT_LIMIT]}'


class TaskTag(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, verbose_name='Тэг'
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name='Задача'
    )

    def __str__(self):
        return f'{self.task} {self.tag}'
    

class Comment(models.Model):
    '''Model for comments.'''
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.content[:TEXT_LIMIT]}'
