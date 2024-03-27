# redirect_api
Простой API для создания пар ключ-значение (keyword - url) и использования этих пар в целях переадресации.

Как развернуть

1. Клонировать репозиторий
2. Перейти в папку infra
3. Созайдте файл .env
4. `docker compose up`

Пример .env:
```.env
# EXAMPLE .env file, change the values to your own
POSTGRES_USER=postgres
POSTGRES_PASSWORD=psql1337
POSTGRES_DB=redirects_api
```

Проект будет доступен на localhost:8000

Примеры запросов

Request:
POST: .../services/
```json
{
    "keyword": "mail",
    "url": "https://mail.ru"
}
```

Response:

```json
{
    "created_at": "2024-03-27T04:42:55.343436",
    "url": "https://mail.ru",
    "updated_at": "2024-03-27T04:42:55.343439",
    "keyword": "mail"
}
```

После запроса выше, переход на
`{app_url}/redirect?service=mail`
перенаправит клиента на
`https://mail.ru/`

Более подробную документацию можно изучить на эндпоинте /docs
По умолчанию: `localhost:8000/docs`




