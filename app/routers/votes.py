from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import Place, Votes
from app.oauth2 import get_current_user
from app.database.pydantic_models import VoteRequest
from sqlalchemy import and_

router = APIRouter(
    prefix='/api',
    tags=['Votes/Likes']
)

@router.post('/vote/{place_id}')
def add_vote( place_id: int, request: VoteRequest,  db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_id = current_user.id

    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with id {place_id} not found"
        )

    is_exists = db.query(Votes).filter(
        and_(Votes.place_id == place_id, Votes.user_id == user_id)
    ).first()

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
    
