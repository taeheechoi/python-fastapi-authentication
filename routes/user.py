from fastapi import status, HTTPException, APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import User
from schema.schema import NewUser, ResUser, Role
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from utils.helpers import hash_password

db = SessionLocal()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

@router.post('/signup/', response_model=ResUser, status_code=status.HTTP_201_CREATED)
async def create_a_user(user: NewUser):
    try:
        hashed_password = await hash_password(user.password)

        new_user = User(
            fullname = user.fullname,
            email = user.email,
            password = hash_password,
            role = user.role,
            date=datetime.now().strftime("%Y-%m-%d"),
            time=datetime.now().strftime("%H:%M:%S"),
        )

        db_item = db.query(User).filter(User.email == new_user.email).first()

        if db_item is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with the email already exists')
        
        db.add(new_user)
        db.commit()
        return new_user


    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An error occurred while creating the user')