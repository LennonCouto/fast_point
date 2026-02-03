import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI

from fast_point.routers import auth, todos, users
from fast_point.schemas import Message

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='FAST POINT')

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá amigos!'}
