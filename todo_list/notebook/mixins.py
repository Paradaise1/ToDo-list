from django.shortcuts import get_object_or_404

from .constants import DISPLAYED_TASKS
from .models import Task, TaskTag


class TaskListMixin:
    model = Task
    template_name = 'notebook/tasks.html'

    paginate_by = DISPLAYED_TASKS


class TaskDispatchMixin:
    model = Task
    template_name = 'notebook/create.html'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Task, pk=kwargs['task_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)
    

class GetContextDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_list = TaskTag.objects.filter(task=self.kwargs.get('task_id'))
        context['tags'] = [item.tag for item in tag_list]
        return context