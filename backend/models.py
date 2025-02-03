from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from backend.database import Base

class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    stack = Column(Integer, default=1000)
    active = Column(Boolean, default=True)
    bet_amount = Column(Integer, default=0)
    game_id = Column(String, ForeignKey("games.id"))
    position = Column(String, nullable=True)

class GameDB(Base):
    __tablename__ = "games"

    id = Column(String, primary_key=True, index=True)
    players = relationship("PlayerDB", backref="game")
    pot = Column(Integer, default=0)
    current_bet = Column(Integer, default=0)
    raise_size = Column(Integer, default=0)
    game_state = Column(String, default="pre-flop")