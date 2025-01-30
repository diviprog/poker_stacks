from typing import Dict, List
from fastapi import APIRouter
from models import Game, Player
import uuid

router = APIRouter()

# Store active games
games: Dict[str, Game] = {}

@router.get("/")
def main() -> Dict[str, str]:
    return {"msg":"Successfully run"}

@router.post("/create-game/")
def create_game(player_names: List[str]) -> Dict[str, str]:
    game_id = str(uuid.uuid4())
    players = [Player(id=i+1, position="Player", stack="1000", active=True) for i, name in enumerate(player_names)]

    new_game = Game(players=players)
    games[game_id] = new_game

    return {"game_id": game_id, "message": "Game created successfully"}

@router.get('/get-game/{game_id}')
def get_game(game_id: str) -> Dict[str, dict]:
    game = games.get(game_id)
    if not game:
        return {"error": "Game not found"}
    
    return {"game_id": game_id, "game_data": game.dict()}

@router.get('/show-active-games/')
def get_all_games() -> Dict[str, Game]:
    return games