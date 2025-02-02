positions = {8:['SB','BB','UTG','+1','LJ','HJ','CO','D'],
             7:['SB','BB','UTG','+1','HJ','CO','D'],
             6:['SB','BB','UTG','+1','CO','D'],
             5:['SB','BB','UTG','CO','D'],
             4:['SB','BB','UTG','D'],
             3:['SB','BB','D'],
             2:['D/SB','BB']
             }

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

    # Sort players by their current positions (ensuring a consistent rotation order)
    sorted_players = sorted(player_positions.items(), key=lambda x: x[1])  # Sort by position name

    # Get new positions from `positions` dictionary
    new_positions = positions[num_players]

    # Assign new positions in a rotated manner
    updated_positions = {}
    for i, (player_id, _) in enumerate(sorted_players):
        updated_positions[player_id] = new_positions[i]

    return updated_positions