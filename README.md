Простой ASGI фреймворк, поддерживающий работу по протоколам HTTP и WebSocket.

Создан с целью показа **взаимодействия по протоколу ASGI напрямую**, без FastAPI, Starlette, etc.
В проекте использован Pydantic для упрощения работы с валидацией.

Запускаться может любым ASGI сервером:

uvicorn

```shell
pip install uvicorn
uvicorn main:app
```

daphne


hypercorn 