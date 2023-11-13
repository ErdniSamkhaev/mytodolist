document.addEventListener('DOMContentLoaded', function() {

  // Функция для редактирования задачи
  window.editTask = function(taskId) {
    // Здесь можно открыть модальное окно для редактирования
    // или перенаправить пользователя на страницу редактирования
    console.log('Редактирование задачи с ID:', taskId);
    // Пример открытия модального окна:
    // $('#editTaskModal').modal('show');
    // Заполнение данных формы в модальном окне:
    // $('#editTaskForm').find('input[name="task_id"]').val(taskId);
  };

 // Функция для удаления задачи
  window.deleteTask = function(taskId) {
    if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
      $.ajax({
        url: '/tasks/delete/' + taskId + '/', // Обновленный URL
        method: 'POST',
        data: {
          'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
          'task_id': taskId
        },
        success: function(response) {
          // Проверка статуса ответа и удаление задачи из DOM
          if (response.status === 'success') {
            document.querySelector('.task-card[data-task-id="' + taskId + '"]').remove();
          }
        },
        error: function() {
          alert('Произошла ошибка при удалении задачи.');
        }
      });
    }
  };

window.toggleTask = function(taskId) {
    $.ajax({
        url: '/tasks/toggle/' + taskId + '/', // Убедись, что URL правильный
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'task_id': taskId
        },
        success: function(response) {
            // Здесь можно добавить код для обновления интерфейса, если нужно
        },
        error: function() {
            alert('Произошла ошибка при изменении статуса задачи.');
        }
    });
};


  window.editTask = function(taskId) {
    // Здесь код для открытия модального окна или перенаправления
    console.log('Редактирование задачи с ID:', taskId);
    // Например, перенаправление:
    window.location.href = '/tasks/edit/' + taskId + '/';
};

});
