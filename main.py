import random
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# ----------------------------
# DATABASE SETUP
# ----------------------------

Base = declarative_base()

engine = create_engine("sqlite:///dungeon_game.db")
Session = sessionmaker(bind=engine)
session = Session()


# ----------------------------
# DATABASE MODELS
# ----------------------------
