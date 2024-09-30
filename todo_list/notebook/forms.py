from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Tag, Task


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label='Tags', queryset=Tag.objects.all()
    )

    class Meta:
        model = Task
        exclude = ('author',)
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        super().clean()
        completed = self.cleaned_data['completed']
        completion_date = self.cleaned_data['completion_date']
        if completion_date < timezone.now() and not completed:
            raise ValidationError(
                'Установите корректную дату выполнения задания.'
            )
