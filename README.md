# poker_stacks

Here’s a comprehensive README.md for your Poker Game API project, covering setup, usage, and API documentation.

🃏 Poker Game API

A FastAPI-powered backend for simulating a poker game, including betting, player management, game state progression, and winner determination.

🚀 Features
	•	🏆 Player Management (Create & track player stacks)
	•	🎲 Betting System (Raise, Call, Fold, Check, All-In)
	•	🔄 Game State Progression (Pre-Flop → Flop → Turn → River → Showdown)
	•	🃏 Community Cards Handling
	•	🎯 Hand Evaluation (Upcoming)

📦 Tech Stack

Technology	Usage
Python	Main programming language
FastAPI	Backend API framework
SQLAlchemy	Database ORM
SQLite/PostgreSQL	Database
Pydantic	Data validation
Trey’s Poker Library	Hand evaluation (upcoming)
React.js (Frontend - Upcoming)	UI for player interaction

📂 Project Structure

poker_stacks/
│── backend/
│   ├── app.py               # FastAPI application
│   ├── database.py          # Database setup (SQLAlchemy)
│   ├── models.py            # Database models
│   ├── routes.py            # API routes
│   ├── logic.py             # Game logic (betting, state updates)
│   ├── create_tables.py     # Initializes the database
│   ├── utils/
│   │   ├── tests.py         # Unit tests for API endpoints
│   ├── __init__.py
│── frontend/ (Upcoming)
│── README.md                # Project documentation
│── requirements.txt         # Python dependencies
│── .gitignore
│── alembic/ (Optional for migrations)

🔧 Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/your-username/poker_stacks.git
cd poker_stacks

2️⃣ Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Setup the Database

python3 -m backend.create_tables

If using Alembic for migrations:

alembic upgrade head

5️⃣ Run the API Server

uvicorn backend.app:app --reload

✅ API will run at: http://127.0.0.1:8000

🔍 API Endpoints

📌 1. Game Management

Method	Endpoint	Description
POST	/create-game/	Create a new poker game
PUT	/next_hand/	Rotate player positions for the next hand
PUT	/next_stage/	Move game state (Pre-Flop → Flop → Turn → River → Showdown)
GET	/get-game/{game_id}	Retrieve game details

Example Request: Create a Game

curl -X POST "http://127.0.0.1:8000/create-game/" -H "Content-Type: application/json" \
    -d '{"players": {"Alice": 1000, "Bob": 1000, "Charlie": 1000}}'

📌 2. Betting Actions

Method	Endpoint	Description
PUT	/bet/	Player places a bet
PUT	/raise/	Player raises the bet
PUT	/call/	Player calls the bet
PUT	/check/	Player checks (no bet)
PUT	/fold/	Player folds
PUT	/all-in/	Player goes all-in

Example Request: Player Bets

curl -X PUT "http://127.0.0.1:8000/bet/" -H "Content-Type: application/json" \
    -d '{"game_id": "1234", "player_id": 1, "amount": 100}'

📌 3. Game Progression

Method	Endpoint	Description
PUT	/next_hand/	Rotate player positions
PUT	/next_stage/	Move game state to the next phase

Example Request: Advance Game State

curl -X PUT "http://127.0.0.1:8000/next_stage/" -H "Content-Type: application/json" \
    -d '{"game_id": "1234"}'

🛠 Running Tests

Run all tests using:

pytest backend/utils/tests.py -v

✅ Tests Included:
	•	Game creation (test_create_game)
	•	Betting (test_bet, test_raise, test_call, test_all_in)
	•	Player actions (test_check, test_fold)
	•	Game progression (test_next_hand, test_next_stage)

🛠 Deployment

🔹 Backend
	•	Option 1: Deploy on Heroku

git push heroku main

	•	Option 2: Deploy on Render

render.yaml  # Define service for FastAPI

	•	Option 3: Docker Deployment

docker build -t poker-game-api .
docker run -p 8000:8000 poker-game-api

🔹 Database
	•	Use SQLite locally (games.db).
	•	Use PostgreSQL for production (Supabase, Heroku).

🔹 Frontend (Upcoming)
	•	React.js for user interface.
	•	WebSockets for real-time updates.

📌 Roadmap

✅ Phase 1: Backend
	•	Game creation
	•	Player management
	•	Betting logic
	•	Game state progression

🔜 Phase 2: Hand Evaluation & Community Cards
	•	Implement card dealing (Flop, Turn, River)
	•	Use Treys Poker Evaluator to determine the winner

🔜 Phase 3: Frontend UI
	•	React.js Interface for betting & game tracking
	•	WebSockets for real-time updates

🔜 Phase 4: Multiplayer & Deployment
	•	Multiplayer functionality (real-time WebSockets)
	•	Production Deployment on Heroku / Render
	•	PostgreSQL Integration

📜 License

MIT License.

🔥 This README gives a full overview of your Poker Game API! Let me know if you need modifications. 🚀♠️