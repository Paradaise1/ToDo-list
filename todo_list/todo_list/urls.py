from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy

from notebook.views import index


User = get_user_model()

urlpatterns = [
    path('', index, name='index'),
    path('', include('notebook.urls', namespace='notebook')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            model=User,
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('notebook:tasks'),
        ),
        name='registration',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
