from sqlalchemy import Column, String, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    hcp_name = Column(String)
    interaction_type = Column(String)
    date = Column(String)
    time = Column(String)
    sentiment = Column(String)
    outcomes = Column(String)
    follow_up = Column(String)

class Material(Base):
    __tablename__ = "materials"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    interaction_id = Column(String, ForeignKey("interactions.id"))
    name = Column(String)
    type = Column(String)

class Sample(Base):
    __tablename__ = "samples"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    interaction_id = Column(String, ForeignKey("interactions.id"))
    product_name = Column(String)
    quantity = Column(Integer)