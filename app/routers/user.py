from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will recieve from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database import models
from app.database.database import engine, get_db
# This is the pydantic validation model
from app.database.pydantic_models import UserCreate
# This is the pydantic response model
from app.database.pydantic_models import UserResponse
models.Base.metadata.create_all(bind=engine)
from app.database.models import User
# password hashing.
from app.utilities.utils import get_hashed_password, check_password

router = APIRouter(
    prefix='/api',
    tags=['Users']
)

@router.post('/create/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(request:UserCreate ,db: Session = Depends(get_db)):

    # hashing the password.
    hashed_password = get_hashed_password(request.password)
    
    request.password = hashed_password

    new_user = User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/get/user/{id}', response_model=UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} do not exists')
    
    return user
