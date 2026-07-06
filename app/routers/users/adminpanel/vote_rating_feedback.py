from fastapi import Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from app.utilities.oauth2 import get_current_user
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.routers.users.adminpanel.pydanticModels import AdminVoteResponse, AdminRatingsResponse, AdminFeedbackResponse
from typing import List
from app.routers.users.adminpanel.db_ops import AdminPanelDbOps
from app.routers.users.adminpanel.helper_function import (
    admin_feedback_response,
    admin_rating_response,
    admin_vote_response,
)


router = APIRouter(
    prefix='/api/admin',
    tags=['Users']
)


def db_ops_init(db: Session = Depends(get_db)):
    return AdminPanelDbOps(db)


# ========================= votes ================================

@router.get('/votes', response_model=List[AdminVoteResponse])
def admin_vote(db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    return admin_vote_response(db_ops, current_user)
    


# ========================= ratings =================================

@router.get('/rating', response_model=List[AdminRatingsResponse])
def admin_rating(db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    return admin_rating_response(db_ops, current_user)


# =============================== feedback ==============================

@router.get('/feedback', response_model=List[AdminFeedbackResponse])
def admin_feedback(db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    return admin_feedback_response(db_ops, current_user)
