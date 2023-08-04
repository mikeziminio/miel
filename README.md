### 🍯 Miel

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

### Why Miel, а не Starlette / FastAPI?

1. Более удобная обработка ошибок
2. 
3. Под капотом родные http.HTTPStatus и http.HTTMPMethod


### TODO

1. Поддержка Lifespan Protocol: https://asgi.readthedocs.io/en/latest/specs/lifespan.html
2. Поддержка ASGI TLS Extension: https://asgi.readthedocs.io/en/latest/specs/tls.html
3. Реализовать FileResponse и StreamingResponse
