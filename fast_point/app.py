from http import HTTPStatus

from fastapi import FastAPI

from fast_point.routers import auth, users
from fast_point.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá amigos!'}
