import json
import typing
import uuid

from pydantic import BaseModel

from src.entities import Card, CardEvent


class ResourceChanges(BaseModel):
    education: int
    friendship: int
    money: int
    health: int


class ManualSwipe(BaseModel):
    title: str
    resource_changes: ResourceChanges


class ManualCard(BaseModel):
    photo_url: str
    name: str
    description: str
    right: ManualSwipe
    left: ManualSwipe


def convert_json_to_cards(filename: str = 'cards.json') -> typing.Iterable[Card]:
    with open(filename, 'r', encoding='utf-8') as f:
        cards = json.load(f)['cards']

    for card in cards:
        manual_card = ManualCard(**card)

        yield Card(
            id=str(uuid.uuid4()),
            photo_url=manual_card.photo_url,
            name=manual_card.name,
            description=manual_card.description,
            left=_convert_manual_swipe_to_event(manual_card.left),
            right=_convert_manual_swipe_to_event(manual_card.right)
        )


def _convert_manual_swipe_to_event(manual_swipe: ManualSwipe) -> CardEvent:
    resources = manual_swipe.resource_changes
    return CardEvent(
        title=manual_swipe.title,
        changes=[resources.education, resources.friendship, resources.money, resources.health]
    )


if __name__ == '__main__':
    for c in convert_json_to_cards():
        print(c)
