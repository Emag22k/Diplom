from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

class RouteCreate(BaseModel):
    origin: str
    destination: str
    price: int

class RouteResponse(BaseModel):
    id: int
    origin: str
    destination: str
    price: int

    class Config:
        orm_mode = True

class TicketCreate(BaseModel):
    route_id: int
    purchase_date: datetime

class TicketResponse(BaseModel):
    id: int
    route_id: int
    user_id: int
    purchase_date: datetime

    class Config:
        orm_mode = True

class LogResponse(BaseModel):
    id: int
    action: str
    timestamp: datetime
    user_id: int

    class Config:
        orm_mode = True
