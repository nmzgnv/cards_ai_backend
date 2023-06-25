import uuid

from pydantic import BaseModel, Field, conlist


class CardEvent(BaseModel):
    title: str
    changes: conlist(int, min_items=4, max_items=4)


class Card(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    photo_url: str
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=0, max_length=500)

    left: CardEvent
    right: CardEvent


card_example = Card(
    photo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/%D0%92%D0%BB%D0%B0%D0%B4_%D0%91%D1%83%D0%BC%D0%B0%D0%B3%D0%B0_%283%29_%D0%BD%D0%B0_VK_Fest_5_%28cropped%29.jpg/800px-%D0%92%D0%BB%D0%B0%D0%B4_%D0%91%D1%83%D0%BC%D0%B0%D0%B3%D0%B0_%283%29_%D0%BD%D0%B0_VK_Fest_5_%28cropped%29.jpg',
    name='Vlad&Slaves',
    description="description",
    left=CardEvent(
        title='left',
        changes=[1, 2, -3, 4]
    ),
    right=CardEvent(
        title='right',
        changes=[-1, -2, 3, -4]
    )
)

if __name__ == '__main__':
    print(card_example.json())
