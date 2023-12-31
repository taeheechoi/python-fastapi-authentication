from fastapi import status, HTTPException, APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import User
from schema.schema import  NewUser, ResUser, Login, Role, DeletionSuccess, ResUpdateUser
from datetime import datetime

from auth.auth import sign_jwt
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from utils.helpers import hash_password, verify_hashed_password, get_user_from_token

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
            password = hashed_password,
            role = user.role,
            date=datetime.now().strftime('%Y-%m-%d'),
            time=datetime.now().strftime('%H:%M:%S'),
        )

        db_item = db.query(User).filter(User.email == new_user.email).first()

        if db_item is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with the email already exists')
        
        db.add(new_user)
        db.commit()
        return new_user


    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An error occurred while creating the user')
    

@router.post('/login/')
async def login_a_user(login: Login):
    try:
        db_user = db.query(User).filter(User.email == login.email).first()

        if db_user is not None:
            is_password_valid = await verify_hashed_password(login.password, db_user.password)

            if not is_password_valid:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You have entered a wrong password.')
            
            if is_password_valid:
                token = sign_jwt(db_user)
                return token
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You have entered a wrong password.')
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found in the database.')
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found in the database.')
    
@router.get('/users/', response_model=List[ResUser], status_code=status.HTTP_200_OK)
async def get_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user_email = user_from_token['user_email']
        offset = (page - 1) * per_page

        if role == Role.ADMIN:
            user_entries = db.query(User).offset(offset).limit(per_page).all()
        elif role == Role.MANAGER:
            user_entries = db.query(User).filter(User.role == Role.USER).offset(offset).limit(per_page).all()
        elif role == Role.USER:
            user_entries = db.query(User).filter(User.email == user_email).first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient privileges')

        return user_entries
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.put('/users/{user_id}/', response_model=ResUpdateUser, status_code=status.HTTP_200_OK)
async def update_user_details(
    user_id: int,
    new_entry: NewUser,
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
       
        role = Role(user_from_token['role'])
        user_email = user_from_token['user_email']

        user_entry_to_update = db.query(User).filter(User.id == user_id).first()
        print(user_entry_to_update)

        if user_entry_to_update is None:
            raise HTTPException(status_code=400, detail=f'User with the id {user_id} was not found')

        if (
            role == Role.ADMIN
            or (role == Role.MANAGER and user_entry_to_update.role == Role.USER)
            or (role == Role.USER and user_entry_to_update.email == user_email)
        ):

            hashed_password = await hash_password(new_entry.password)
            
            user_entry_to_update.fullname = new_entry.fullname
            user_entry_to_update.email = new_entry.email
            user_entry_to_update.password = hashed_password
            user_entry_to_update.date = datetime.now().strftime('%Y-%m-%d')
            user_entry_to_update.time = datetime.now().strftime('%H:%M:%S')
            user_entry_to_update.role = new_entry.role

            db.commit()

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient privileges')

        return user_entry_to_update

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete('/users/{user_id}/', response_model=DeletionSuccess, status_code=status.HTTP_200_OK)
async def delete_user_detail(
    user_id: int,
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user_email = user_from_token['user_email']

        user_entry_to_delete = db.query(User).filter(User.id == user_id).first()

        if user_entry_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {user_id} was not found')

        if (
            role == Role.ADMIN
            or (role == Role.MANAGER and user_entry_to_delete.role == Role.USER)
            or (role == Role.USER and user_entry_to_delete.email == user_email)
        ):
            db.delete(user_entry_to_delete)
            db.commit()

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient privileges')

        return DeletionSuccess()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='User deletion was not successful')

user_routes = router