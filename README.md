# Bookstore API

Это проект API для управления книгами и авторами. Он использует Django и Django REST Framework для предоставления RESTful API для работы с моделями `Book` и `Author`.

## Технологии

- Python
- Django
- Django REST Framework
- Swagger

## Установка

### 1. Клонировать репозиторий

```
git clone git@github.com:TeenCreek/bookstore.git
```

### 2. Создать виртуальное окружение

```
py -m venv venv
. venv\Scripts\activate
```

### 3. Установить зависимости

```
pip install -r requirements.txt
```

### 5. Применить миграции

```
python manage.py migrate
```

### 6. Запустить сервер

```
python manage.py runserver

API будет доступен по адресу: http://127.0.0.1:8000/api/
```

## Эндпоинты

- GET /api/books - возвращает список книг
- POST /api/books - создает новую книгу
- PUT /api/books/{id} - редактирует книгу
- POST /api/books/{id}/buy - апи для покупки книги, уменьшает счетчик count если он положительный или возвращает ошибку
- GET /api/authors - возвращает список авторов
- POST /api/authors - создает нового автора
- PUT /api/authors/{id} - редактирует автора

## Пример запросов

1. Создание автора

```
POST /api/authors/
{
  "first_name": "John",
  "last_name": "Doe"
}
```

2. Создание книги

```
POST /api/books/
{
  "title": "New Book",
  "author": {
    "first_name": "John",
    "last_name": "Doe"
  },
  "count": 10
}
```

3. Обновление книги

```
PUT /api/books/1/
{
  "title": "Updated Book Title",
  "count": 15,
  "author": {
    "first_name": "John",
    "last_name": "Doe"
  }
}
```
