# Poker Game API

A FastAPI-powered backend service for simulating poker games with comprehensive player management, betting systems, and game state tracking.

## Features

* **Player Management**: Create and track player stacks, handle player actions
* **Comprehensive Betting System**: Support for raise, call, fold, check, and all-in actions
* **Game State Management**: Handle progression through pre-flop, flop, turn, river, and showdown
* **Community Cards**: Manage and deal community cards
* **Hand Evaluation**: Determine winning hands (upcoming feature)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI |
| Database | SQLAlchemy (ORM), SQLite/PostgreSQL |
| Data Validation | Pydantic |
| Hand Evaluation | Treys Poker Library (upcoming) |
| Frontend | React.js (upcoming) |

## Project Structure

```
poker_stacks/
│── backend/
│   ├── app.py               # FastAPI application
│   ├── database.py          # Database setup
│   ├── models.py            # Database models
│   ├── routes.py            # API routes
│   ├── logic.py             # Game logic
│   ├── create_tables.py     # Database initialization
│   ├── utils/
│   │   ├── tests.py         # Unit tests
│   ├── __init__.py
│── frontend/               # Upcoming
│── README.md
│── requirements.txt
│── .gitignore
│── alembic/                # Optional for migrations
```

## Installation

### Prerequisites
* Python 3.x
* pip package manager
* Virtual environment (recommended)

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/your-username/poker_stacks.git
cd poker_stacks
```

2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize database
```bash
python3 -m backend.create_tables
# If using Alembic:
alembic upgrade head
```

5. Start the server
```bash
uvicorn backend.app:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

### Game Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create-game/` | Create a new poker game |
| PUT | `/next_hand/` | Rotate player positions |
| PUT | `/next_stage/` | Progress game state |
| GET | `/get-game/{game_id}` | Get game details |

Example: Creating a game
```bash
curl -X POST "http://127.0.0.1:8000/create-game/" \
     -H "Content-Type: application/json" \
     -d '{"players": {"Alice": 1000, "Bob": 1000, "Charlie": 1000}}'
```

### Betting Actions

| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/bet/` | Place a bet |
| PUT | `/raise/` | Raise existing bet |
| PUT | `/call/` | Call current bet |
| PUT | `/check/` | Check (no bet) |
| PUT | `/fold/` | Fold hand |
| PUT | `/all-in/` | Go all-in |

Example: Player betting
```bash
curl -X PUT "http://127.0.0.1:8000/bet/" \
     -H "Content-Type: application/json" \
     -d '{"game_id": "1234", "player_id": 1, "amount": 100}'
```

## Testing

Run the test suite:
```bash
pytest backend/utils/tests.py -v
```

Test coverage includes:
* Game creation and management
* Betting actions
* Player actions
* Game state progression

## Deployment Options

### Backend Deployment

1. **Heroku**
```bash
git push heroku main
```

2. **Render**
* Configure `render.yaml` for service definition

3. **Docker**
```bash
docker build -t poker-game-api .
docker run -p 8000:8000 poker-game-api
```

### Database Options
* Development: SQLite
* Production: PostgreSQL (via Supabase or Heroku)

## Development Roadmap

### ✅ Phase 1: Core Backend
* Game creation and management
* Player management
* Betting logic
* Game state progression

### 🔄 Phase 2: Game Logic
* Card dealing implementation
* Hand evaluation using Treys
* Winner determination

### 📱 Phase 3: Frontend Development
* React.js user interface
* Real-time updates via WebSockets

### 🚀 Phase 4: Production Features
* Multiplayer support
* Production deployment
* PostgreSQL integration

## License

This project is licensed under the MIT License.
