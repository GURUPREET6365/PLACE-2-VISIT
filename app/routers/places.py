from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will recieve from the client.
from typing import Optional, List
from sqlalchemy.orm import Session
# First creating the instance of the fast api for easy use, we can also do it like:
# Creating the table that we created in model.py
from app.database import models
from app.database.database import engine, get_db
# This is the pydantic validation model
from app.database.pydantic_models import Places, UserCreate
# This is the pydantic response model
from app.database.pydantic_models import responsePlace, UserResponse
models.Base.metadata.create_all(bind=engine)
from app.database.models import Place
from app.oauth2 import get_current_user

router = APIRouter(
    prefix='/api',
    tags=['Place']
)

# This is returning a list so we need to use List from typing library.
@router.get('/all/place', status_code=status.HTTP_200_OK, response_model=List[responsePlace])
def all_place(db: Session = Depends(get_db)):
    place = db.query(Place).all()
    return place


@router.post('/add/place', status_code=status.HTTP_201_CREATED, response_model=responsePlace)
def create_place(request: Places, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # print(request.model_dump())
    # This is going to first convert into dict and then unpack it.

    # Checking that the place_name or place
    print(current_user.email)

    place = Place(**request.model_dump())
    db.add(place)
    db.commit()
    # This refresh is for when the data is returned, then it will first refresh db and then return so that all data should go and this store the data in place
    db.refresh(place)
    return place


@router.get('/place/{id}')
def specfic_place(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    place = db.query(Place).filter(Place.id == id).all()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'place':place} 


@router.post('/place/delete/{id}')
def delete_place(id:int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    place_query = db.query(Place).filter(Place.id == id) # This always return some query, so it can't be empty.
    # .first() always return orm, if found and none if not found.
    place = place_query.first()
    print(place)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The place of the id:{id} is not found.')
    
    else:
        place_query.delete(synchronize_session=False)
        print('This place is deleted.')
        db.commit()

        return {'success':'The place has been deleted.'}
    
@router.post('/place/update/{id}')
def update_place(request:Places, id:int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    place_query = db.query(Place).filter(Place.id == id)
    place = place_query.first()

    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The place of the id:{id} is not found.')
    
    place_query.update(request.model_dump(), synchronize_session=False)
    db.commit()

    return {'success':'post updated.'}
