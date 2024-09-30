from rest_framework import viewsets

from api.serializers import (
    TagSerializer,
    TaskSerializer,
)
from api.permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from notebook.models import Tag, Task


class TaskViewSet(viewsets.ModelViewSet):
    '''ViewSet for tasks.'''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''ViewSet for tags.'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
