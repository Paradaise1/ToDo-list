from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse, reverse_lazy

from .constants import DISPLAYED_TASKS
from .forms import TaskForm
from .mixins import TaskDispatchMixin, TaskListMixin, GetContextDataMixin
from .models import Tag, Task
from .utils import get_query_set


User = get_user_model()


def index(request):
    '''View for main page.'''
    return render(request, 'notebook/index.html')


class TaskListView(LoginRequiredMixin, TaskListMixin, ListView):
    '''Viewset for tasks.'''
    def get_queryset(self):
        return get_query_set(Task.objects, self)


class CompletedTaskListView(LoginRequiredMixin, TaskListMixin, ListView):
    '''Viewset for completed tasks.'''
    def get_queryset(self):
        return get_query_set(Task.objects, self).filter(completed=True)


class UncompletedTaskListView(LoginRequiredMixin, TaskListMixin, ListView):
    '''Viewset for uncompleted tasks.'''
    def get_queryset(self):
        return get_query_set(Task.objects, self).filter(completed=False)


class TagListView(LoginRequiredMixin, ListView):
    '''Viewset for tags.'''
    model = Task
    template_name = 'notebook/tag.html'

    def get_queryset(self):
        return get_query_set(Task.objects, self).filter(
            tasktag__tag__slug=self.kwargs.get('tag_slug')
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(
            Tag,
            slug=self.kwargs.get('tag_slug'),
        )
        return context

    paginate_by = DISPLAYED_TASKS


class TaskCreateView(LoginRequiredMixin, CreateView):
    '''Viewset for create tasks.'''
    model = Task
    form_class = TaskForm
    template_name = 'notebook/create.html'

    # def get_queryset(self):
    #     return Task.objects.prefetch_related('tags')

    def get_success_url(self):
        return reverse('notebook:tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, TaskDispatchMixin, UpdateView):
    '''Viewset for update tasks.'''
    form_class = TaskForm

    def get_success_url(self):
        return reverse(
            'notebook:task_detail',
            kwargs={'task_id': self.kwargs.get('task_id')}
        )

    def get_object(self):
        return get_object_or_404(
            Task,
            pk=self.kwargs.get('task_id'),
            author=self.request.user
        )


class TaskDetailView(LoginRequiredMixin, GetContextDataMixin, DetailView):
    '''Viewset for detail informatin for tasks.'''
    model = Task
    template_name = 'notebook/detail.html'

    def get_queryset(self):
        return get_query_set(Task.objects, self)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), pk=self.kwargs.get('task_id')
        )


class TaskDeleteView(
    LoginRequiredMixin,
    TaskDispatchMixin,
    GetContextDataMixin,
    DeleteView
):
    '''Viewset for delete tasks.'''
    queryset = Task.objects.prefetch_related('tags')
    success_url = reverse_lazy('notebook:tasks')

    def get_object(self):
        return get_object_or_404(
            self.queryset,
            pk=self.kwargs.get('task_id'),
            author=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        context['form'] = TaskForm(
            self.request.POST, instance=instance
        )
        return context
