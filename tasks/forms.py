from django import forms
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple
from .models import Task
import datetime


class TaskForm(forms.ModelForm):
    """Класс TaskForm
Этот класс наследуется от forms.ModelForm и представляет форму для создания или редактирования объектов Task.

Внутренний класс Meta содержит мета-информацию для класса TaskForm.

Атрибуты класса Meta:
model: Ссылка на модель, которую представляет эта форма. В данном случае, это модель Task.
fields: Список полей, которые должны быть включены в форму. Определяет следующие поля модели Task:
'title': Поле для ввода названия задачи.
'completed': Флажок, указывающий на то, выполнена задача или нет.
'priority': Выпадающий список для выбора приоритета задачи.
'tags': Поле для выбора тегов, которые могут быть связаны с задачей.
SelectDateWidget используется для создания удобного интерфейса выбора даты. empty_label позволяет установить
плейсхолдеры для каждого из выпадающих списков (год, месяц, день), а years определяет диапазон лет,
доступных для выбора.
CheckboxSelectMultiple используется для поля tags, чтобы отображать теги в виде чекбоксов, что может быть более удобно
 для пользователя, чем стандартный множественный выбор.

Использование TaskForm:
Для использования TaskForm необходимо создать экземпляр этой формы в представлении Django и предоставить ему экземпляр
HttpRequest в случае POST запроса, или создать пустой экземпляр формы для GET запроса.
Сохранение формы приведет к созданию или обновлению записи Task в базе данных."""
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
        fields = ['title', 'completed', 'priority', 'tags', 'deadline']
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }
