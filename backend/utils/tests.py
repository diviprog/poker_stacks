import sys
import os

# Ensure backend directory is in Python's module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi.testclient import TestClient #type:ignore
from backend.app import app  # Correct absolute import

client = TestClient(app)

# Global variable to store game_id for testing
game_id = None


# ✅ Test Creating a Game
def test_create_game():
    global game_id
    response = client.post("/create-game/", json={"players": {"Alice": 1000, "Bob": 1000}})
    assert response.status_code == 200
    data = response.json()
    game_id = data["game_id"]  # Store game_id for future tests
    assert "game_id" in data
    assert data["message"] == "Game created successfully"


# ✅ Test Checking (Allowed)def test_check_allowed():
    response = client.put("/check/", json={"game_id": game_id, "player_id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Player 1 checked"


# ✅ Test Checking (Not Allowed - Active Bet)
def test_check_not_allowed():
    client.put("/bet/", json={"game_id": game_id, "player_id": 2, "amount": 100})  # Player 2 bets $100
    response = client.put("/check/", json={"game_id": game_id, "player_id": 1})  # Player 1 tries to check
    assert response.status_code == 400  # Now it should correctly return 400
    assert response.json()["detail"] == "Cannot check. You must call or raise."


# ✅ Test Betting (Valid Bet)
def test_bet():
    response = client.put("/bet/", json={"game_id": game_id, "player_id": 1, "amount": 100})
    assert response.status_code == 200
    assert "Player 1 bet 100" in response.json()["message"]


# ✅ Test Betting (Invalid - Not Enough Stack)
def test_bet_insufficient_stack():
    response = client.put("/bet/", json={"game_id": game_id, "player_id": 1, "amount": 5000})
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stack"


# ✅ Test Calling (Matching Bet)
def test_call():
    response = client.put(f"/call/?game_id={game_id}&player_id=2")
    assert response.status_code == 200
    assert "Player 2 called" in response.json()["message"]


# ✅ Test Raising (Valid Raise)
def test_raise():
    response = client.put(f"/raise/?game_id={game_id}&player_id=1&raise_amount=200")
    assert response.status_code == 200
    assert "Player 1 raised to 200" in response.json()["message"]


# ✅ Test Raising (Invalid - Below Minimum Raise)
def test_raise_invalid():
    response = client.put(f"/raise/?game_id={game_id}&player_id=2&raise_amount=150")  # Below min raise
    assert response.status_code == 400
    assert "Raise must be at least" in response.json()["detail"]


# ✅ Test Folding
def test_fold():
    response = client.put(f"/fold/?game_id={game_id}&player_id=2")
    assert response.status_code == 200
    assert "Player 2 has folded" in response.json()["message"]


# ✅ Test All-in
def test_all_in():
    response = client.put(f"/all-in/?game_id={game_id}&player_id=1")
    assert response.status_code == 200
    assert "Player 1 went all-in" in response.json()["message"]


# ✅ Test Next Round (Resets Betting)
def test_next_round():
    response = client.put(f"/next-round/?game_id={game_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Next betting round has started"

def test_next_stage():
    """Test advancing game state through Flop, Turn, River, and Showdown"""

    for expected_state in ["flop", "turn", "river", "showdown"]:
        response = client.put("/next_stage/", json={"game_id": game_id})
        assert response.status_code == 200
        assert response.json()["new_state"] == expected_state

def test_next_hand():
    """Test position rotation after each hand"""

    response = client.put("/next_hand/", json={"game_id": str(game_id)})  # Ensure it's a string
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert "new_positions" in data
    assert data["message"] == "Positions updated for next hand"
    assert isinstance(data["new_positions"], dict)  # Ensure it's a dictionary

# ✅ Test End Game Session
def test_end_game():
    response = client.delete(f"/end-session/{game_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Game {game_id} and all associated players have been deleted"