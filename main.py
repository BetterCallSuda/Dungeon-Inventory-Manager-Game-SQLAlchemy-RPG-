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


def add_item(player, item_name, quantity):

    item = session.query(Inventory).filter_by(
        player_id=player.id,
        item_name=item_name
    ).first()

    if item:
        item.quantity += quantity
    else:
        item = Inventory(
            item_name=item_name,
            quantity=quantity,
            player_id=player.id
        )
        session.add(item)

    session.commit()


# ----------------------------
# TREASURE EVENT
# ----------------------------

def find_treasure(player):

    gold = random.randint(5, 20)

    print("\n💰 You found treasure!")
    print("Gold gained:", gold)

    player.gold += gold
    add_item(player, "Gold Coin", gold)

    session.commit()


# ----------------------------
# MONSTER BATTLE
# ----------------------------

def fight_monster(player):

    monster = session.query(Monster).order_by(
        random.random()
    ).first()

    monster_health = monster.health

    print(f"\n👹 A {monster.name} appears!")
    print("Monster Health:", monster.health)

    while monster_health > 0 and player.health > 0:

        action = input("\nFight (f) or Run (r): ")

        if action == "r":
            print("You escaped!")
            return

        player_attack = random.randint(5, 15)
        monster_health -= player_attack

        print("You hit the monster for", player_attack)

        if monster_health <= 0:
            print("Monster defeated! 🏆")

            player.gold += 10
            player.level += 1

            battle = Battle(
                monster_name=monster.name,
                result="Win",
                player_id=player.id
            )

            session.add(battle)
            session.commit()

            return

        monster_attack = monster.damage
        player.health -= monster_attack

        print("Monster hits you for", monster_attack)
        print("Your health:", player.health)

    if player.health <= 0:
        print("\n💀 You were defeated!")

        battle = Battle(
            monster_name=monster.name,
            result="Lose",
            player_id=player.id
        )

        session.add(battle)
        session.commit()

        exit()


# ----------------------------
# ROOM EXPLORATION
# ----------------------------

def explore_room(player):

    event = random.choice(["monster", "treasure", "trap"])

    if event == "monster":
        fight_monster(player)

    elif event == "treasure":
        find_treasure(player)

    else:
        damage = random.randint(5, 15)
        player.health -= damage

        print("\n⚠️ Trap triggered!")
        print("Damage:", damage)
        print("Health left:", player.health)

        session.commit()


# ----------------------------
# MAIN GAME LOOP
# ----------------------------

def game_loop(player):

    while True:

        print("\n===== DUNGEON MENU =====")
        print("1. Explore Dungeon")
        print("2. View Stats")
        print("3. Inventory")
        print("4. Exit Game")

        choice = input("Choose option: ")

        if choice == "1":
            explore_room(player)

        elif choice == "2":
            show_stats(player)

        elif choice == "3":
            show_inventory(player)

        elif choice == "4":
            print("Game saved. Goodbye!")
            break

        else:
            print("Invalid choice")


# ----------------------------
# START GAME
# ----------------------------

def main():

    create_monsters()

    print("==== DUNGEON RPG ====")

    player = create_player()

    game_loop(player)


if __name__ == "__main__":
    main()
