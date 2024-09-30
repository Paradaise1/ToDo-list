from django.contrib import admin

from .models import Tag, Task


admin.site.empty_value_display = 'Не задано'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''Admin's model for tags.'''
    list_display = ('name', 'slug')
    list_editable = ('name',)
    list_display_links = ('slug',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    '''Admin's model for tasks.'''
    list_display = (
        'title',
        'description',
        'completed',
        'completion_date',
        'author',
        'tags',
    )
    list_display = ('title', 'description', 'completed', 'completion_date')
    list_editable = ('description',)
    search_fields = ('title',)
    list_filter = ('title',)
    list_display_links = ('title',)
