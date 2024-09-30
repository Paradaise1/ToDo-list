from django.urls import path

from . import views


app_name = 'notebook'

urlpatterns = [
    path('tasks/', views.TaskListView.as_view(),
         name='tasks'),
    path('tasks/completed/', views.CompletedTaskListView.as_view(),
         name='completed_tasks'),
    path('tasks/uncompleted/', views.UncompletedTaskListView.as_view(),
         name='uncompleted_tasks'),
    path('tags/<slug:tag_slug>/', views.TagListView.as_view(),
         name='tag_tasks'),     
    path('tasks/create/', views.TaskCreateView.as_view(),
         name='create_task'),
    path('tasks/<int:task_id>/', views.TaskDetailView.as_view(),
         name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.TaskUpdateView.as_view(),
         name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.TaskDeleteView.as_view(),
         name='delete_task'),
]