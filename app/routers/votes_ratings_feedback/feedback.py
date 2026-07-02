from fastapi import status, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import Feedback
from app.database.pydantic_models import FeedbackRequest

router = APIRouter(
    prefix='/api',
    tags=['ratings']
)


@router.post('/feedback', status_code=status.HTTP_201_CREATED)
def feedback(request:FeedbackRequest, db: Session = Depends(get_db)):
    # creating a new row in db.
    new_feedback = Feedback(**request.model_dump())
    db.add(new_feedback)
    db.commit()
    return {"message":"feedback accepted successfully"}
