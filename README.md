## Описание

Файл task_1.py – решение 1 части тестового задания

Папка task_2 – решение 2 части тестового задания

## Автор проекта

[Mikhail](https://github.com/tooMike)

## Установка и запуск Django проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tooMike/test_project_1
```

```
cd test_project_1/task_2
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Спецификация

При локальном запуске документация будет доступна по адресу:

```
http://127.0.0.1:8000/redoc/
```

## Основные технические требования

Python==3.9

## Эндпоинты

`/api/users/` – регистрация нового пользователя (метод `POST`)

`/api/auth/token/login/` – получение токена (метод `POST`)

`/api/categories/` – получение списка категорий с подкатегориями (метод `GET`)

`/api/products/` – получение списка товаров (метод `GET`)

`/api/cart/`

- добавление товара в корзину (метод `POST`)
- получение списка всех товаров в корзине (метод `GET`)
- удаление товара из корзины (метод `DELETE`)
- изменение количества товара в корзине (метод `PATCH`)

`/api/cart/clean/` – удаление всех товаров из корзины (метод `DELETE`)




## Примеры запросов к API

### Регистрация нового пользователя

Тип запроса: `POST`

Эндпоинт: `/api/users/`

Права доступа: Доступно всем пользователям.

Обязательные параметры: `username, password`

Пример запрос:

```
{
    "username": "root",
    "password": "root12345"
}
```

Пример ответа:

```
{
    "username": "root"
}
```

### Получение токена

Эндпоинт: `/api/auth/token/login/`

Права доступа: Доступно всем пользователям.

Тип запроса: `POST`

Обязательные параметры: `username, password`

Пример запроса: 

```
{
    "username": "root",
    "password": "root12345"
}
```

Пример ответа:

```
{
    "auth_token": "7bb4199224770e7e36f413d76bcf645bf06b1b43"
}
```

### Получение списка товаров

Эндпоинт: `/api/products/`

Права доступа: Доступно всем пользователям.

Тип запроса: `GET`

Пример ответа:

```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Товар 1",
            "slug": "tovar1",
            "category": "Категория 1",
            "subcategory": "Подкатегория 1",
            "price": "42.00",
            "images": [
                "http://127.0.0.1:8000/media/product/img1.png",
                "http://127.0.0.1:8000/media/product/img2.png",
                "http://127.0.0.1:8000/media/product/img3.png"
            ]
        },
        ...
    ]
}
```