class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    health = Column(Integer)
    level = Column(Integer)
    gold = Column(Integer)
