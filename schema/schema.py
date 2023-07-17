from pydantic import BaseModel
from typing import Optional
from enum import Enum
from dataclasses import dataclass
# contain the declarations for our available data schemas, including response and request bodies

class Role(str, Enum):
    USER = 'user'
    MANAGER = 'manager'
    ADMIN = 'admin'

@dataclass
class SignUser:
    fullname: str
    email: str
    role: Role

class NewUser(BaseModel):
    fullname: str
    email: str
    password: str
    role: Role

    class Config:
        orm_mode = True


class ResUser(BaseModel):
    id: int
    fullname: str
    email: str
    role: Role
    date: str
    time: str

    class Config:
        orm_mode = True


class ResUpdateUser(BaseModel):
    id: int
    fullname: str
    email: str
    # password: str
    role: Role
    date: str
    time: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class NewEntry(BaseModel):
    text: str
    number_of_calories: Optional[int]

    class Config:
        orm_mode = True

class ResEntry(BaseModel):
    id: int
    date: str
    number_of_calories: str
    text: str
    time: str
    is_under_calories: bool
    user: str

    class Config:
        orm_mode = True

class DeletionSuccess(BaseModel):
    status: str = 'Success'
    message: str = 'User deleted successfully'