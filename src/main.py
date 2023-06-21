import random
import uuid
from copy import copy
import uvicorn
from fastapi import FastAPI, APIRouter, Request, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from entities import Card, CardEvent
from src.cards_adapter import convert_json_to_cards
from src.settings import AppSettings

settings = AppSettings(secret_key=str(uuid.uuid4()))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, https_only=True)
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
async def return_cards() -> list[Card]:
    k = min(len(cards), 5)
    return random.sample(cards, k)


@api_router.post('/swipe')
async def update_resources(request: Request, card_id: str = Body(embed=True),
                           direction: str = Body(embed=True, regex='(right)|(left)')) -> list[int]:
    card = card_by_id.get(card_id)
    if not card:
        raise HTTPException(status_code=400, detail='Card not found')

    event: CardEvent = getattr(card, direction)
    current_resources = _get_resources(request)
    new_resources = _apply_changes(current_resources, event.changes)
    request.session['resources'] = new_resources
    return new_resources


@api_router.get('/resources')
async def get_resources(request: Request) -> list[int]:
    return _get_resources(request)


def _get_resources(request: Request) -> list[int]:
    resources = request.session.get('resources')
    return resources if resources else [0] * 4


def _apply_changes(current_resources: list[int], changes: list[int]) -> list[int]:
    if len(current_resources) != len(changes):
        raise ValueError('Current resources and changes length mismatch')

    current_resources = copy(current_resources)
    for i in range(len(current_resources)):
        new_value = current_resources[i] + changes[i]
        current_resources[i] = max(min(new_value, 100), -100)

    return current_resources


app.include_router(api_router)

if __name__ == '__main__':
    # uvicorn main:app --host 127.0.0.1 --port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")
