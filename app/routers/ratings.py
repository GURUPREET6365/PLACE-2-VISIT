from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import User, Ratings
from app.oauth2 import get_current_user
from app.database.pydantic_models import RatingsRequest
from sqlalchemy import and_

router = APIRouter(
    prefix='/api',
    tags=['ratings']
)

# This endpoint for ratings.
@router.post('/place/rating/{place_id}', status_code=status.HTTP_201_CREATED)
def place_rating(place_id:int,  request:RatingsRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # print(request)
    user_id = current_user.id
    # Here I am using query for direct update of the already contained row of db, as query has command update.
    ratings_query = db.query(Ratings).filter(and_(Ratings.user_id==user_id, Ratings.place_id==place_id))
    ratings = ratings_query.first()
    if ratings:
        # If ratings is already done, then update the new ratings.
        # print("going to update the rating")
        request.user_id = user_id
        request.place_id = place_id
        # print(request)
        ratings_query.update(request.model_dump(), synchronize_session=False)
        db.commit()
        return {"message":"rating successfully updated"}
    else:
        # creating new ratings in memory
        # now giving the user id and place id in request pydantic model
        request.user_id = user_id
        request.place_id = place_id
        rating = Ratings(**request.model_dump())
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return {"message":"rating successfully created"}
