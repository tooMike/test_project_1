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