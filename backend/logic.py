positions = {8:['SB','BB','UTG','+1','LJ','HJ','CO','D'],
             7:['SB','BB','UTG','+1','HJ','CO','D'],
             6:['SB','BB','UTG','+1','CO','D'],
             5:['SB','BB','UTG','CO','D'],
             4:['SB','BB','UTG','D'],
             3:['SB','BB','D'],
             2:['D/SB','BB']
             }

GAME_STATES = ["pre-flop", "flop", "turn", "river", "showdown"]

def update_positions(player_positions: dict) -> dict:
    """Rotates player positions for the next hand.

    Args:
        player_positions (dict): A dictionary mapping `player_id` to their current position.

    Returns:
        dict: A dictionary mapping `player_id` to their new position.
    """
    num_players = len(player_positions)

    # Validate number of players
    if num_players not in positions:
        return {"error": "Invalid number of players"}

    # Ensure all players have valid positions before sorting
    if any(pos is None for pos in player_positions.values()):
        return {"error": "Player positions are not set"}

    # Sort players by their current positions (ensuring a consistent rotation order)
    sorted_players = sorted(player_positions.items(), key=lambda x: positions[num_players].index(x[1]))

    # Rotate positions
    rotated_positions = {
        p_id: positions[num_players][(i + 1) % num_players]
        for i, (p_id, _) in enumerate(sorted_players)
    }

    return rotated_positions

def get_next_state(current_state: str) -> str:
    """Returns the next state in the game"""
    if current_state not in GAME_STATES:
        return "error"
    
    current_index = GAME_STATES.index(current_state)
    
    # If already in showdown, stay there
    if current_index == len(GAME_STATES) - 1:
        return "showdown"

    return GAME_STATES[current_index + 1]