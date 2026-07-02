from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from app.utilities.oauth2 import get_current_user
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import Votes, Ratings, Feedback
from app.routers.users.adminpanel.pydanticModels import AdminVoteResponse, AdminRatingsResponse, AdminFeedbackResponse
from typing import List


router = APIRouter(
    prefix='/api/admin',
    tags=['Users']
)

# ========================= votes ================================

@router.get('/votes', response_model=List[AdminVoteResponse])
def admin_vote(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin':
        votes = db.query(Votes).all()
        return votes
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')
    


# ========================= ratings =================================

@router.get('/rating', response_model=List[AdminRatingsResponse])
def admin_rating(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin':
        ratings = db.query(Ratings).all()
        return ratings
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="unauthorized user")


# =============================== feedback ==============================

@router.get('/feedback', response_model=List[AdminFeedbackResponse])
def admin_feedback(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin' or role == 'staff':
        feedback = db.query(Feedback).all()
        return feedback
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized user")
