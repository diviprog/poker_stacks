from fastapi import FastAPI
from models import Player, Game

app = FastAPI()

# In-memory storage for simplicity
games = {}

@app.post("/create-game/")
def create_game(player_names: list[str]):
    game_id = len(games) + 1
    players = [Player(name=name, stack=1000) for name in player_names]
    games[game_id] = {"players": players}
    return {"game_id": game_id, "players": players}

@app.put("/update-stack/")
def update_stack(game_id: int, player_name: str, change: int):
    game = games.get(game_id)
    if not game:
        return {"error": "Game not found"}

    for player in game["players"]:
        if player.name == player_name:
            player.stack += change
            return {"message": "Stack updated", "player": player}

    return {"error": "Player not found"}