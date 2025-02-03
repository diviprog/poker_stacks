from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from backend.models import GameDB, PlayerDB
from backend.database import get_db
from backend.logic import update_positions, get_next_state, positions
import uuid
from pydantic import BaseModel # type: ignore

router = APIRouter()

class BetRequest(BaseModel):
    game_id: str
    player_id: int
    amount: int

class CheckRequest(BaseModel):
    game_id: str
    player_id: int

class NextHandRequest(BaseModel):
    game_id: str

class NextStageRequest(BaseModel):
    game_id: str

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
    new_game = GameDB(id=game_id, game_state="pre-flop")
    db.add(new_game)
    db.commit()

    num_players = len(player_data.players)
    if num_players not in positions:
        raise HTTPException(status_code=400, detail="Invalid number of players for a game.")

    position_list = positions[num_players]

    # Add players
    for i, (name, stack) in enumerate(player_data.players.items()):
        player = PlayerDB(
            name=name,
            stack=stack,
            active=True,
            game_id=game_id,
            position=position_list[i]  # ✅ Now correctly aligned with zero-based index
        )
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
        "state": game.game_state,
        "pot": game.pot,
        "current_bet": game.current_bet,
        "players": [{"id": p.id, "name": p.name, "stack": p.stack, "active": p.active} for p in players]
    }

@router.get('/show-active-games/')
def get_all_games(db: Session = Depends(get_db)) -> Dict[str, list]:
    """Retrieve all active games"""
    
    games = db.query(GameDB).all()
    return {"games": [{"game_id": g.id} for g in games]}

@router.delete("/end-session/{game_id}")
def end_game_session(game_id: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Deletes a game and all associated players"""
    
    game = db.query(GameDB).filter(GameDB.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.query(PlayerDB).filter(PlayerDB.game_id == game_id).delete()
    db.delete(game)  # ✅ Delete game directly
    db.commit()

    return {"message": f"Game {game_id} and all associated players have been deleted"}

@router.put("/check/")
def check(request: CheckRequest, db: Session = Depends(get_db)):
    """Player checks (takes no action, does not bet)"""

    player = db.query(PlayerDB).filter(
        PlayerDB.id == request.player_id, PlayerDB.game_id == request.game_id
    ).first()
    game = db.query(GameDB).filter(GameDB.id == request.game_id).first()

    if not player or not game:
        raise HTTPException(status_code=404, detail="Player or Game not found")
    
    if not player.active:
        raise HTTPException(status_code=400, detail="Player has already folded")

    # 🚀 Ensure a check is only possible when there is NO active bet
    if game.current_bet > 0 and player.bet_amount < game.current_bet:
        raise HTTPException(status_code=400, detail="Cannot check. You must call or raise.")

    return {"message": f"Player {request.player_id} checked"}

@router.put("/bet/")
def place_bet(request: BetRequest, db: Session = Depends(get_db)):
    """Player places a bet, reducing their stack and adding to the pot"""

    player = db.query(PlayerDB).filter(
        PlayerDB.id == request.player_id, PlayerDB.game_id == request.game_id
    ).first()
    game = db.query(GameDB).filter(GameDB.id == request.game_id).first()

    if not player or not game:
        raise HTTPException(status_code=404, detail="Player or Game not found")

    if player.stack < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient stack")

    if request.amount < game.current_bet + game.raise_size:
        raise HTTPException(status_code=400, detail=f"Bet must be at least {game.current_bet + game.raise_size}")

    # Deduct stack and update pot
    player.stack -= request.amount
    game.pot += request.amount
    game.current_bet = max(request.amount, game.current_bet)

    # Update player's bet for the round
    player.bet_amount = request.amount

    db.commit()
    return {"message": f"Player {request.player_id} bet {request.amount}. Remaining stack: {player.stack}, Pot: {game.pot}"}

@router.put("/raise/")
def place_raise(game_id: str, player_id: int, raise_amount: int, db: Session = Depends(get_db)):
    """Player raises the bet, increasing the pot and setting a new highest bet"""

    player = db.query(PlayerDB).filter(PlayerDB.id == player_id, PlayerDB.game_id == game_id).first()
    game = db.query(GameDB).filter(GameDB.id == game_id).first()

    if not player or not game:
        raise HTTPException(status_code=404, detail="Player or Game not found")

    # Ensure `raise_size` exists in GameDB
    if not hasattr(game, "raise_size"):
        raise HTTPException(status_code=500, detail="raise_size is not defined in GameDB")

    if player.stack < raise_amount:
        raise HTTPException(status_code=400, detail="Insufficient stack to raise")

    if raise_amount < game.current_bet + game.raise_size:
        raise HTTPException(status_code=400, detail=f"Raise must be at least {game.current_bet + game.raise_size}")

    # Deduct stack and update pot
    difference = raise_amount - player.bet_amount  # Only deduct the additional amount
    player.stack -= difference
    game.pot += difference

    # Update game bet information
    game.raise_size = raise_amount - game.current_bet  # Update the raise size
    game.current_bet = raise_amount  # Update the highest bet

    # Update player's bet amount
    player.bet_amount = raise_amount

    db.commit()
    return {"message": f"Player {player_id} raised to {raise_amount}. Remaining stack: {player.stack}, Pot: {game.pot}"}

@router.put("/fold/")
def fold(game_id: str, player_id: int, db: Session = Depends(get_db)):
    """Player folds and is removed from the round"""
    
    player = db.query(PlayerDB).filter(PlayerDB.id == player_id, PlayerDB.game_id == game_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if not player.active:
        raise HTTPException(status_code=400, detail="Player has already folded")

    player.active = False  # Mark player as folded
    db.commit()
    return {"message": f"Player {player_id} has folded"}

@router.put("/call/")
def call_bet(game_id: str, player_id: int, db: Session = Depends(get_db)):
    """Player calls the current bet amount"""

    player = db.query(PlayerDB).filter(PlayerDB.id == player_id, PlayerDB.game_id == game_id).first()
    game = db.query(GameDB).filter(GameDB.id == game_id).first()

    if not player or not game:
        raise HTTPException(status_code=404, detail="Player or Game not found")

    call_amount = game.current_bet - player.bet_amount

    if player.stack < call_amount:
        call_amount = player.stack  # Player goes all-in

    player.stack -= call_amount
    game.pot += call_amount
    player.bet_amount = game.current_bet

    db.commit()
    return {"message": f"Player {player_id} called with {call_amount}. Remaining stack: {player.stack}, Pot: {game.pot}"}

@router.put("/all-in/")
def all_in(game_id: str, player_id: int, db: Session = Depends(get_db)):
    """Player goes all-in, betting their entire stack"""

    player = db.query(PlayerDB).filter(PlayerDB.id == player_id, PlayerDB.game_id == game_id).first()
    game = db.query(GameDB).filter(GameDB.id == game_id).first()

    if not player or not game:
        raise HTTPException(status_code=404, detail="Player or Game not found")
    
    if player.bet_amount == player.stack:
        raise HTTPException(status_code=400, detail="Player is already all-in")

    all_in_amount = player.stack

    # Deduct stack and update pot
    game.pot += all_in_amount
    player.stack = 0
    player.bet_amount += all_in_amount

    # Update current bet if this is the highest
    if all_in_amount > game.current_bet:
        game.current_bet = all_in_amount

    db.commit()
    return {"message": f"Player {player_id} went all-in with {all_in_amount}. Pot: {game.pot}"}

@router.put("/next-round/")
def next_round(game_id: str, db: Session = Depends(get_db)):
    """Moves to the next betting round and resets player bet amounts"""

    game = db.query(GameDB).filter(GameDB.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Reset player bet amounts for the next round
    players = db.query(PlayerDB).filter(PlayerDB.game_id == game_id).all()
    for player in players:
        player.bet_amount = 0

    game.current_bet = 0  # Reset the current bet
    game.raise_size = 0

    db.commit()
    return {"message": "Next betting round has started"}

@router.put("/next_stage/")
def next_stage(request:NextStageRequest, db: Session = Depends(get_db)):
    """Moves the game to the next stage (Flop, Turn, River, Showdown)"""

    game = db.query(GameDB).filter(GameDB.id == request.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.game_state == "showdown":
        raise HTTPException(status_code=400, detail="Game is already at showdown")
    
    new_state = get_next_state(game.game_state)

    if new_state == "error":
        raise HTTPException(status_code=400, detail="Invalid game state")

    game.game_state = new_state
    db.commit()

    return {"message": f"Game moved to {new_state}", "new_state": new_state}

@router.put("/next_hand/")
def next_hand(request:NextHandRequest, db: Session = Depends(get_db)):
    """Updates player positions for the next hand"""

    # Fetch game and players
    game = db.query(GameDB).filter(GameDB.id == request.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    players = db.query(PlayerDB).filter(PlayerDB.game_id == request.game_id).all()
    if not players:
        raise HTTPException(status_code=400, detail="No players found in game")

    # Convert players into dictionary `{player_id: position}` for `update_positions()`
    player_positions = {p.id: p.position for p in players}

    # Get updated positions
    updated_positions = update_positions(player_positions)

    # Handle errors from `logic.py`
    if "error" in updated_positions:
        raise HTTPException(status_code=400, detail=updated_positions["error"])

    # Update player positions in the database
    for player in players:
        player.position = updated_positions[player.id]
    
    game.game_stage = "pre-flop"
    game.pot = 0
    game.current_bet = 0
    for player in players:
        player.bet_amount = 0

    db.commit()
    
    return {"message": "Positions updated for next hand", "new_positions": updated_positions}