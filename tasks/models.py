from django.db import models
from django.conf import settings


class Task(models.Model):
    """
    Класс Task представляет собой модель задачи в системе управления задачами.

    Атрибуты:
        title (CharField): Название задачи.
            max_length=200 - Максимальная длина названия задачи составляет 200 символов.
        completed (BooleanField): Статус выполнения задачи.
            default=False - По умолчанию, задача помечается как невыполненная.
        created (DateTimeField): Дата и время создания задачи.
            auto_now_add=True - Дата и время будут автоматически установлены при создании задачи.
        priority (CharField): Приоритет задачи.
            max_length=10 - Максимальная длина поля приоритета составляет 10 символов.
            choices=PRIORITY_CHOICES - Поле приоритета имеет ограниченный выбор значений.
            default='medium' - По умолчанию, задаче присваивается средний приоритет.
        tags (ManyToManyField): Теги, присвоенные задаче.
            blank=True - Поле может быть пустым.
        deadline (DateTimeField): Срок выполнения задачи.
            null=True, blank=True - Поле может быть пустым и не содержать значения.
        owner (ForeignKey): Владелец задачи, связанный с пользователем системы.
            settings.AUTH_USER_MODEL - Ссылка на модель пользователя, используемая в проекте.
            on_delete=models.CASCADE - При удалении пользователя удаляются и его задачи.

    PRIORITY_CHOICES: Кортеж кортежей, представляющий доступные варианты для выбора приоритета задачи.
        ('low', 'Low') - Низкий приоритет.
        ('medium', 'Medium') - Средний приоритет.
        ('high', 'High') - Высокий приоритет.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    tags = models.ManyToManyField('Tag', blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Tag(models.Model):
    """
    Класс Tag представляет собой модель тега в системе управления задачами.

    Атрибуты:
        name (CharField): Название тега.
            max_length=50 - Максимальная длина названия тега составляет 50 символов.
    """
    name = models.CharField(max_length=50)
