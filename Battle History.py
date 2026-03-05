class Battle(Base):
    __tablename__ = "battles"

    id = Column(Integer, primary_key=True)
    monster_name = Column(String)
    result = Column(String)
    player_id = Column(Integer)
