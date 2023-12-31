from fastapi import status, HTTPException, APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import Entry
from schema.schema import ResEntry, NewEntry, Role, DeletionSuccess
from datetime import datetime
from typing import List
from config.config import settings
from sqlalchemy.exc import SQLAlchemyError
from utils.helpers import get_calories_from_api, get_user_from_token


db = SessionLocal()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

@router.post('/user/entries/', response_model=ResEntry, status_code=status.HTTP_201_CREATED)
async def save_entires(entry: NewEntry, token: str = Depends(oauth2_scheme)):
    try:

        user_from_token = await get_user_from_token(token)
        print(user_from_token)
        user = user_from_token['user_id']
        print(user)

        if entry.number_of_calories is None:
            calories = await get_calories_from_api()
            entry.number_of_calories = calories

        new_entry = Entry(
            text=entry.text,
            number_of_calories = entry.number_of_calories,
            user=user,
            date=datetime.now().strftime('%Y-%m-%d'),
            time=datetime.now().strftime('%H:%M:%S'),
            is_under_calories =False
        )
        
        if entry.number_of_calories is not None and int(entry.number_of_calories) < int(settings.EXPECTED_CALORIES_PER_DAY):
            new_entry.is_under_calories = True

        db.add(new_entry)
        db.commit()

        return new_entry
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Entry was not saved to the database.')
    

@router.get('/user/entries/', response_model=List[ResEntry], status_code=status.HTTP_200_OK)
async def get_entries(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user = user_from_token['user_id']
        offset = (page - 1) * per_page

        print(Role.USER.value)
    
        if role == Role.USER:
            all_entries = db.query(Entry).filter(Entry.user == user).offset(offset).limit(per_page).all()
        elif role == Role.ADMIN:
            all_entries = db.query(Entry).offset(offset).limit(per_page).all()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User with the role specified was not found.')
        
        return all_entries
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error while quering the database.')

@router.put('/user/entries/{entry_id}/', response_model=ResEntry, status_code=status.HTTP_200_OK)
async def update_entries(entry_id: int, entry: NewEntry, token: str = Depends(oauth2_scheme)):
    try:
        user_from_token = await get_user_from_token(token)
        
        role = Role(user_from_token['role'])
        entry_to_update = db.query(Entry).filter(Entry.id == entry_id).first()

        if entry_to_update is None:
            raise HTTPException(status_code=400, detail=f"Entry with the id {entry_id} was not found")

        if role == Role.USER or role == Role.ADMIN:
            entry_to_update.text = entry.text
            entry_to_update.number_of_calories = entry.number_of_calories
            entry_to_update.date = datetime.now().strftime("%Y-%m-%d")
            entry_to_update.time = datetime.now().strftime("%H:%M:%S")

        db.commit()
        return entry_to_update
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete('/user/entries/{entry_id}/', response_model=DeletionSuccess, status_code=status.HTTP_200_OK)
async def delete_an_entry(entry_id: int, token: str = Depends(oauth2_scheme)):
    try:
        user_from_token = await get_user_from_token(token)
        print(user_from_token)
        role = Role(user_from_token['role'])
        user = user_from_token['user_id']
        
        entry_to_delete = db.query(Entry).filter(Entry.id == entry_id).first()

        if entry_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Entry with the given id {entry_id} is not found')

        if (role == Role.USER and entry_to_delete.user == user) or role == Role.ADMIN:
            db.delete(entry_to_delete)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient privileges')

        return DeletionSuccess()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail='Entity deletion was not successful')


entry_routes = router
