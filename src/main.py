import random
import uuid
from copy import copy
from typing import Annotated
import uvicorn
from fastapi import FastAPI, APIRouter, Request, HTTPException, Body, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from entities import Card, CardEvent
from src.cards_adapter import convert_json_to_cards
from src.settings import AppSettings

settings = AppSettings(secret_key=str(uuid.uuid4()))

SESSION_KEY = 'session'
MAX_AGE = 14 * 24 * 60 * 60  # 14 days, in seconds

app = FastAPI()
app.add_middleware(
    SessionMiddleware, session_cookie=SESSION_KEY, secret_key=settings.secret_key
)

origins = [
    'http://localhost',
    'http://localhost:63342',
    'http://127.0.0.1',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
    'http://185.87.50.169',
    'http://185.87.50.169:3000',
    'http://185.87.50.169:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter(prefix='/api')

cards = []
card_by_id: dict[str, Card] = dict()


@app.on_event('startup')
async def on_startup():
    global cards, card_by_id
    cards = list(convert_json_to_cards('cards.json'))
    card_by_id = {card.id: card for card in cards}


@api_router.get('/')
async def root() -> dict:
    return {"message": "Hello World"}


@api_router.get('/cards')
async def return_cards(request: Request, count: int = Query(5, gt=0, lt=20)) -> list[Card]:
    request.session['_init'] = True
    k = min(len(cards), count)
    return random.sample(cards, k)


class InvalidOperation(Exception):
    pass


@api_router.post('/swipe')
async def update_resources(request: Request, card_id: str = Body(embed=True),
                           direction: str = Body(embed=True, regex='(right)|(left)')) -> list[int]:
    card = card_by_id.get(card_id)
    if not card:
        raise HTTPException(status_code=400, detail='Card not found')

    event: CardEvent = getattr(card, direction)
    current_resources = _get_resources(request)
    try:
        new_resources = _apply_changes(current_resources, event.changes)
    except InvalidOperation as e:
        request.session.clear()
        raise HTTPException(status_code=400, detail='Game over') from e

    request.session['resources'] = new_resources
    return new_resources


@api_router.get('/resources')
async def get_resources(request: Request) -> list[int]:
    return _get_resources(request)


def _get_resources(request: Request) -> list[int]:
    resources = request.session.get('resources')
    return resources if resources else [50] * 4


def _apply_changes(current_resources: list[int], changes: list[int]) -> list[int]:
    if len(current_resources) != len(changes):
        raise ValueError('Current resources and changes length mismatch')

    current_resources = copy(current_resources)
    for i in range(len(current_resources)):
        new_value = current_resources[i] + changes[i]
        if new_value <= 0:
            raise InvalidOperation('Resources cant be lower than 0')
        current_resources[i] = min(new_value, 100)

    return current_resources


app.include_router(api_router)

if __name__ == '__main__':
    # uvicorn main:app --host 127.0.0.1 --port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")
