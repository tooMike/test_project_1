# Описание

Файл task_1.py – решение 1 части тестового задания
Папка task_2 – решение 2 части тестового задания

# Установка и запуск

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/kittygram2plus.git
```

```
cd kittygram2plus
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


Регистрация пользователя:/api/auth/users/
{
    "username": "root",
    "password": "root12345"
}
Пример ответа:
{
    "email": "",
    "username": "root2",
    "id": 2
}

Получение токена:  /api/auth/token/login/
Пример запроса: 
{
    "username": "root",
    "password": "root12345"
}
Пример ответа:
{
    "auth_token": "7bb4199224770e7e36f413d76bcf645bf06b1b43"
}