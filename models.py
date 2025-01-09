from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    tickets = relationship("Ticket", back_populates="owner")
    logs = relationship("Log", back_populates="user")

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String)
    destination = Column(String)
    price = Column(Integer)

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    purchase_date = Column(DateTime)
    owner = relationship("User", back_populates="tickets")

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="logs")
