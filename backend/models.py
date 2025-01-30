from typing import List, Dict

from pydantic import BaseModel

class Player(BaseModel):
    id: int
    position: str
    stack: str
    active: bool

class Game(BaseModel):
    players: List[Player]