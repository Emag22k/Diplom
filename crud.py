from sqlalchemy.orm import Session
from models import User, Route, Ticket, Log
from schemas import UserCreate, RouteCreate, TicketCreate
import bcrypt
from datetime import datetime

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def create_route(db: Session, route: RouteCreate):
    db_route = Route(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

def update_route(db: Session, route_id: int, route: RouteCreate):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if db_route:
        db_route.origin = route.origin
        db_route.destination = route.destination
        db_route.price = route.price
        db.commit()
        db.refresh(db_route)
    return db_route

def delete_route(db: Session, route_id: int):
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if db_route:
        db.delete(db_route)
        db.commit()
    return db_route

def create_ticket(db: Session, ticket: TicketCreate, user_id: int):
    db_ticket = Ticket(route_id=ticket.route_id, user_id=user_id, purchase_date=ticket.purchase_date)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_ticket(db: Session, ticket_id: int, ticket: TicketCreate):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket:
        db_ticket.route_id = ticket.route_id
        db_ticket.purchase_date = ticket.purchase_date
        db.commit()
        db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
    return db_ticket

def log_action(db: Session, user_id: int, action: str):
    log_entry = Log(action=action, timestamp=datetime.utcnow(), user_id=user_id)
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
