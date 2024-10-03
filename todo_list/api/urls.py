from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, TaskViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
