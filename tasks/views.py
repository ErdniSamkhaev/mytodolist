from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse


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


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)  # Убедись, что задача принадлежит пользователю
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return JsonResponse({'status': 'success'})
    return render(request, 'tasks/confirm_delete.html', {'task': task})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'status': 'success'})
