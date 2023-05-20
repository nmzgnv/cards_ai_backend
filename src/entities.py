from pydantic import BaseModel, Field


class ResourceDelta(BaseModel):
    resource_id: int
    delta: int = Field(ge=-100, le=100)


class Card(BaseModel):
    photo_url: str
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=0, max_length=500)

    changes: list[ResourceDelta]


card_example = Card(
    photo_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/%D0%92%D0%BB%D0%B0%D0%B4_%D0%91%D1%83%D0%BC%D0%B0%D0%B3%D0%B0_%283%29_%D0%BD%D0%B0_VK_Fest_5_%28cropped%29.jpg/800px-%D0%92%D0%BB%D0%B0%D0%B4_%D0%91%D1%83%D0%BC%D0%B0%D0%B3%D0%B0_%283%29_%D0%BD%D0%B0_VK_Fest_5_%28cropped%29.jpg',
    name='Vlad&Slaves',
    description="description",
    changes=[
        ResourceDelta(resource_id=0, delta=50),
        ResourceDelta(resource_id=1, delta=50),
        ResourceDelta(resource_id=2, delta=-30),
        ResourceDelta(resource_id=3, delta=0),
    ]
)

if __name__ == '__main__':
    print(card_example.json())
