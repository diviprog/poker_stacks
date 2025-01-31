from typing import Dict, List
from fastapi import APIRouter, Depends # type: ignore
from sqlalchemy.orm import Session # type: ignore
from models import GameDB, PlayerDB
from database import get_db
import uuid
from pydantic import BaseModel # type: ignore

router = APIRouter()

@router.get("/")
def main() -> Dict[str, str]:
    return {"msg": "Successfully run"}

# Define Pydantic model for input validation
class PlayerInput(BaseModel):
    players: Dict[str, int]  # Dictionary of {player_name: stack}

@router.post("/create-game/")
def create_game(player_data: PlayerInput, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Creates a new game and stores it in the database"""

    game_id = str(uuid.uuid4())
    new_game = GameDB(id=game_id)
    db.add(new_game)
    db.commit()

    # Add players
    for name, stack in player_data.players.items():
        player = PlayerDB(name=name, stack=stack, active=True, game_id=game_id)
        db.add(player)
    
    db.commit()
    return {"game_id": game_id, "message": "Game created successfully"}

@router.get('/get-game/{game_id}')
def get_game(game_id: str, db: Session = Depends(get_db)) -> Dict[str, dict]:
    """Retrieve an existing game from the database"""
    
    game = db.query(GameDB).filter(GameDB.id == game_id).first()
    if not game:
        return {"error": "Game not found"}
    
    players = db.query(PlayerDB).filter(PlayerDB.game_id == game_id).all()
    return {
        "game_id": game_id,
        "players": [{"id": p.id, "name": p.name, "stack": p.stack, "active": p.active} for p in players]
    }

@router.get('/show-active-games/')
def get_all_games(db: Session = Depends(get_db)) -> Dict[str, list]:
    """Retrieve all active games"""
    
    games = db.query(GameDB).all()
    return {"games": [{"game_id": g.id} for g in games]}

@router.delete("/end-session/{game_id}")
def end_game_session(game_id: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Deletes a game and all associated players from the database"""
    
    game = db.query(GameDB).filter(GameDB.id == game_id).first()
    if not game:
        return {"error": "Game not found"}

    # Delete all players in the game
    db.query(PlayerDB).filter(PlayerDB.game_id == game_id).delete()

    # Delete the game itself
    db.query(GameDB).filter(GameDB.id == game_id).delete()

    db.commit()

    return {"message": f"Game {game_id} and all associated players have been deleted"}