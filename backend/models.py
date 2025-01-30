from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from database import Base

class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    stack = Column(Integer, default=1000)
    active = Column(Boolean, default=True)
    game_id = Column(String, ForeignKey("games.id"))

class GameDB(Base):
    __tablename__ = "games"

    id = Column(String, primary_key=True, index=True)
    players = relationship("PlayerDB", backref="game")