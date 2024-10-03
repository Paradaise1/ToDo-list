# ToDo-list

## Сервис для управления задачами.

## Описание

Приложение ToDo-list позволяет пользователям прохождении регистрации простматривать список всех своих задач (в томм чиле по тэгам) и комментариев к ним, <br/>
а так же создавать новые задачи и оставлять свои комментарии.

## **Запуск проекта в dev-режиме**
### Для запуска в dev-режиме необходим файл с переменными окружения .env
Инструкция ориентирована на операционную систему windows и утилиту git bash.<br/>
Для прочих инструментов используйте аналоги команд для вашего окружения.

Клонировать репозиторий:

```
git clone https://github.com/Paradaise1/car_shop.git
```

```
cd todo_list
```

Запустить docker-compose файл:

```
docker compose up --build
```
Теперь по адресу `http://127.0.0.1:8000/` будут доступны следующие эндпоинты (обрабатываются Django-сервисом):

POST /api/auth/users/ - зарегестрировать нового пользователя.
POST /api/auth/users/me/ - получить/обновить зарегестрированного пользователя.
POST /api/auth/jwt/create/ - создать JWT-токен.
POST /api/auth/jwt/refresh/ - получить новый JWT по истечении времени жизни ранее сгенерированного.

GET /api/tasks/ — получение списка задач.
GET /api/tasks/<task_id>/ — получение информации о конкретной задаче.
GET /api/tags/ — получение списка доступных тэгов для задач.
POST /api/tasks/ — создание новой задачи.
PUT /api/tasks/<task_id>/ — обновление информации о задаче.
DELETE /api/tasks/<task_id>/ — удаление задачи.

А так же по адресу `http://127.0.0.1:8080/` будут доступны следующие эндпоинты (обрабатываются FastAPI-сервисом):
*Для использования FastAPI сервиса для начала нужно получить JWT-токен на Django-сервисе*

GET /api/tasks/<task_id>/comments/ — получение комментариев к задаче.
GET /api/tasks/<task_id>/comments/<comment_id> — получение отдельного комментария к задаче.
POST /api/tasks/<task_id>/comments/ — добавление нового комментария к задаче.
PUT /api/tasks/<task_id>/comments/<comment_id> — обновление информации о комментарии.
DELETE /api/tasks/<task_id>/comments/<comment_id> — удаление комментария.

GET /docs - документация, сгенерированная FastAPI-сервисом

## Примеры запросов и ответов:

*Регистрация:*
**POST**```/api/auth/users/```
```
{
    "username": "string",
    "password": "string"
}
```
Ответ:
```
{
    "email": "string",
    "username": "string",
    "id": "int"
}
```

*Создать JWT токен:*
**POST**```/api/auth/jwt/create/```
```
{
    "username": "string",
    "password": "string"
}
```
Ответ:
```
{
    "refresh": "string",
    "access": "string"
}
```

*Ключевое слово для передачи JWT-токена - Bearer*

*Создать задачу:*
**POST**```/api/tasks/```
```
{
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "completion_date": "datetime",
    "tags": [
        "id": "int"
    ]
}
```
Ответ:
```
{
    "id": "int",
    "author": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "completion_date": "datetime",
    "tags": [
        "id": "int",
        "name": "string"
    ]
}
```

*Создать комментарий:*
**POST**```/api/tasks/{task_id}/comments/```
```
{
    "content": "string"
}
```
Ответ:
```
{
    "content": "string"
}
```

*Получить информацию о конкретном автомобиле:*
**GET**```/api/tasks/{id}/```

Ответ:
```
{
    "id": "int",
    "author": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "completion_date": "datetime",
    "tags": [
        "id": "int",
        "name": "string"
    ]
}
```

### Автор проекта: Роот Артём
