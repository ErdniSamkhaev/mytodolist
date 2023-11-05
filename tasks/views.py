from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def home(request):
    return render(request, 'registration/home.html')


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)  # Получаем задачи только для текущего пользователя
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Сохраняем форму без коммита в базу данных
            task.owner = request.user  # Устанавливаем владельца задачи
            task.save()  # Теперь сохраняем задачу в базу данных
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/list.html', {'tasks': tasks, 'form': form})


def signup(request):
    """
    Представление для регистрации нового пользователя.
    Обрабатывает GET и POST запросы.

    Параметры:
    - request: HttpRequest - объект запроса от Django.

    Процесс:
    - При POST запросе: получает данные из формы регистрации, валидирует их и, если данные корректны,
      регистрирует нового пользователя, выполняет вход и перенаправляет на список задач.
    - При GET запросе: создает новую форму регистрации.

    Возвращает:
    - HttpResponse с рендером шаблона 'registration/signup.html', передавая форму регистрации.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def toggle_task(request, task_id):
    """
    Представление для переключения статуса задачи (выполнено/не выполнено).
    Обрабатывает POST запросы.

    Параметры:
    - request: HttpRequest - объект запроса от Django.
    - task_id: int - идентификатор задачи, статус которой нужно изменить.

    Процесс:
    - Использует get_object_or_404 для поиска задачи по id.
    - Изменяет статус задачи на противоположный и сохраняет изменения.
    - Перенаправляет на список задач.

    Возвращает:
    - HttpResponse с перенаправлением на представление списка задач.
    """
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
