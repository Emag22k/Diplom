from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, TicketCreate, UserResponse, TicketResponse
from crud import create_user, update_user, delete_user, create_ticket, update_ticket, delete_ticket, log_action
from auth import get_current_user
from models import User

user_router = APIRouter( prefix="/users", tags=["users"])

@user_router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@user_router.put("/me", response_model=UserResponse)
def update_my_data(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = update_user(db, current_user.id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    log_action(db, user_id=current_user.id, action="Updated user data")
    return updated_user

@user_router.delete("/me")
def delete_my_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_user = delete_user(db, current_user.id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    log_action(db, user_id=current_user.id, action="Deleted account")
    return {"msg": "Account deleted"}

@user_router.post("/tickets/", response_model=TicketResponse)
def buy_ticket(ticket: TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_ticket(db, ticket, current_user.id)

@user_router.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_my_ticket(ticket_id: int, ticket: TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_ticket = update_ticket(db, ticket_id, ticket)
    log_action(db, user_id=current_user.id, action="Updated ticket")
    return updated_ticket

@user_router.delete("/tickets/{ticket_id}")
def delete_my_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_ticket = delete_ticket(db, ticket_id)
    log_action(db, user_id=current_user.id, action="Deleted ticket")
    return {"msg": "Ticket deleted"}
