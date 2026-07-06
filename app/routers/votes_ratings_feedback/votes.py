from fastapi import Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.utilities.oauth2 import get_current_user
from app.routers.votes_ratings_feedback.pydanticModels import VoteRequest
from app.routers.votes_ratings_feedback.db_ops import VoteRatingFeedbackDbOps
from app.routers.votes_ratings_feedback.helper_function import add_vote_response

router = APIRouter(
    prefix='/api',
    tags=['Votes/Likes']
)


def db_ops_init(db: Session = Depends(get_db)):
    return VoteRatingFeedbackDbOps(db)


@router.post('/vote/{place_id}')
def add_vote(
    place_id: int,
    request: VoteRequest,
    db_ops: Session = Depends(db_ops_init),
    current_user = Depends(get_current_user)
):
    return add_vote_response(place_id, request, db_ops, current_user)
    
