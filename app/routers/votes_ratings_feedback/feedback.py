from fastapi import status, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.routers.votes_ratings_feedback.pydanticModels import FeedbackRequest
from app.routers.votes_ratings_feedback.db_ops import VoteRatingFeedbackDbOps
from app.routers.votes_ratings_feedback.helper_function import feedback_response

router = APIRouter(
    prefix='/api',
    tags=['ratings']
)


def db_ops_init(db: Session = Depends(get_db)):
    return VoteRatingFeedbackDbOps(db)


@router.post('/feedback', status_code=status.HTTP_201_CREATED)
def feedback(request: FeedbackRequest, db_ops: Session = Depends(db_ops_init)):
    return feedback_response(request, db_ops)
