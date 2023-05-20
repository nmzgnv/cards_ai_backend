import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from entities import Card, card_example

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix='/api')


@api_router.get('/')
async def root() -> dict:
    return {"message": "Hello World"}


@api_router.get('/hello/{name}')
async def say_hello(name: str) -> dict:
    return {"message": f"Hello {name}"}


@api_router.get('/cards')
async def return_cards() -> list[Card]:
    return [card_example] * 20


app.include_router(api_router)

if __name__ == '__main__':
    # uvicorn main:app --host 127.0.0.1 --port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")
