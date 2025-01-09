from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, RouteCreate, UserResponse, RouteResponse
from crud import create_user, update_user, delete_user, create_route, update_route, delete_route, get_user, log_action

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.post("/users/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user

@admin_router.put("/users/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    log_action(db, user_id=user_id, action="Updated user")
    return updated_user

@admin_router.delete("/users/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    log_action(db, user_id=user_id, action="Deleted user")
    return {"msg": "User deleted"}

@admin_router.post("/routes/", response_model=RouteResponse)
def create_new_route(route: RouteCreate, db: Session = Depends(get_db)):
    return create_route(db, route)

@admin_router.put("/routes/{route_id}", response_model=RouteResponse)
def update_existing_route(route_id: int, route: RouteCreate, db: Session = Depends(get_db)):
    return update_route(db, route_id, route)

@admin_router.delete("/routes/{route_id}")
def delete_existing_route(route_id: int, db: Session = Depends(get_db)):
    return delete_route(db, route_id)
