class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    damage = Column(Integer)
    health = Column(Integer)
