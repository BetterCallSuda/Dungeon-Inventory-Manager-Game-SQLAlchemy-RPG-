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

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    health = Column(Integer)
    level = Column(Integer)
    gold = Column(Integer)

    inventory = relationship("Inventory", back_populates="player")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    quantity = Column(Integer)

    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="inventory")


class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    health = Column(Integer)
    damage = Column(Integer)


class Battle(Base):
    __tablename__ = "battles"

    id = Column(Integer, primary_key=True)
    monster_name = Column(String)
    result = Column(String)
    player_id = Column(Integer)


Base.metadata.create_all(engine)


# ----------------------------
# INITIAL MONSTERS
# ----------------------------

def create_monsters():
    if session.query(Monster).count() == 0:

        monsters = [
            Monster(name="Goblin", health=30, damage=5),
            Monster(name="Skeleton", health=40, damage=7),
            Monster(name="Orc", health=60, damage=10),
            Monster(name="Dark Knight", health=80, damage=15),
        ]

        session.add_all(monsters)
        session.commit()


# ----------------------------
# CREATE PLAYER
# ----------------------------

def create_player():

    name = input("Enter your hero name: ")

    player = Player(
        name=name,
        health=100,
        level=1,
        gold=0
    )

    session.add(player)
    session.commit()

    print(f"\nWelcome {name}! Your adventure begins.\n")

    return player


# ----------------------------
# SHOW PLAYER STATS
# ----------------------------

def show_stats(player):

    print("\n---- PLAYER STATS ----")
    print("Name:", player.name)
    print("Health:", player.health)
    print("Level:", player.level)
    print("Gold:", player.gold)
    print("----------------------\n")


# ----------------------------
# INVENTORY SYSTEM
# ----------------------------

def show_inventory(player):

    print("\n---- INVENTORY ----")

    items = session.query(Inventory).filter_by(player_id=player.id).all()

    if not items:
        print("Inventory empty")

    for item in items:
        print(item.item_name, "x", item.quantity)

    print("-------------------\n")

