from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will recieve from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import User, Votes
from app.oauth2 import get_current_user
from app.database.pydantic_models import VoteRequest


router = APIRouter(
    prefix='/api',
    tags=['Votes/Likes']
)

@router.post('/add/vote/{user_id}/{place_id}')
def add_vote(user_id: int, place_id: int, request: VoteRequest,  db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    is_exists = db.query(Votes).filter(Votes.place_id == place_id and Votes.user_id==user_id ).first()

    if is_exists is None:

        vote = Votes(
            user_id=user_id,
            place_id=place_id,
            vote = request.vote
        )
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return {'success':True}
    
    # if it is not empty then only update the vote.
    is_exists.vote = request.vote
    db.commit()
    return {'success':True}
    