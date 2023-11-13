from django import forms
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple
from .models import Task
import datetime


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        label='Напишите свою задачу',
        widget=forms.Textarea(attrs={
            'id': 'task_title',
            'name': 'title',
            'placeholder': 'Описание задачи',
            'class': 'form-control',  # Добавь свои классы для стилизации
            'rows': 3,
            'style': 'width: 100%;'  # Или используй inline стили для изменения ширины
        })
    )
    deadline = forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                                       years=range(datetime.datetime.now().year,
                                                                   datetime.datetime.now().year + 10)), required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Task.tags.through.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'priority', 'tags', 'deadline']
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }
