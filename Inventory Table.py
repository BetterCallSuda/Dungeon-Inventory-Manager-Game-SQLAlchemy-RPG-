
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    quantity = Column(Integer)
    player_id = Column(Integer, ForeignKey("players.id"))
