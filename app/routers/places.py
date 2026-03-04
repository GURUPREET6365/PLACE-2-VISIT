from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from typing import List
from sqlalchemy.orm import Session
# First creating the instance of the fast api for easy use, we can also do it like:
# Creating the table that we created in model.py
from app.database import models
from app.database.database import get_db
# This is the pydantic validation model
from app.database.pydantic_models import Places
# This is the pydantic response model
from app.database.pydantic_models import AllPlaceResponse, AdminUpdatePlace, SpecificPlaceResponseModel
from app.database.models import Place, Votes, Ratings
from app.oauth2 import get_current_user, get_current_user_optional
from sqlalchemy import and_
from app.utilities.utils import calculate_vote, all_place_response, calculate_average_rating_all_categories

# models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix='/api',
    tags=['Place']
)

# This is returning a list so we need to use List from typing library.
@router.get('/all/place', status_code=status.HTTP_200_OK, response_model=List[AllPlaceResponse])
def all_place(db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):

    # Finding average rating of overall categories
    place = all_place_response(current_user, db)
    return place

"""
Depends is the function which tells that first run and give me the result then run next function.
"""

@router.post('/add/place', status_code=status.HTTP_201_CREATED)
def create_place(request: Places, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # print(request.model_dump())
    # This is going to first convert into dict and then unpack it.

    # Checking that the place_name or place
    role = current_user.role
    if role == 'staff' or role == 'admin':
        place = Place(**request.model_dump())
        db.add(place)
        db.commit()
        # This refresh is for when the data is returned, then it will first refresh db and then return so that all data should go and this store the data in place.
        db.refresh(place)
        return {"message":"place created successfully"}

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

@router.get('/place/{id}', response_model=SpecificPlaceResponseModel)
def specific_place(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    place = db.query(Place).filter(Place.id == id).first()

    # Calculate votes for this place only.
    like, dislike = calculate_vote(
        db.query(Votes).filter(Votes.place_id == id).all()
    )

    # place is not available of that id then run this
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # if place is available then run this
    vote = db.query(Votes).filter(and_(Votes.user_id == current_user.id, Votes.place_id == id)).first()

    rating = db.query(Ratings).filter(Ratings.place_id == place.id).all()

    # It is return 9 things because of specific place, so we are using indexing
    ratings = calculate_average_rating_all_categories(rating)

    is_user_rated = db.query(Ratings).filter(and_(Ratings.user_id == current_user.id, Ratings.place_id == place.id)).first()

    place_with_vote = {
        "place_name": place.place_name,
        "place_address": place.place_address,
        "about_place": place.about_place,
        "pincode": place.pincode,
        "created_at": place.created_at,
        "id": place.id,
        "voted": vote.vote if vote else None,
        "num_likes": like,
        "num_dislikes": dislike,

        "overall": ratings[1],
        "cleanliness": ratings[2],
        "safety": ratings[3],
        "crowd_behavior": ratings[4],
        "transport_access": ratings[5],
        "lightning": ratings[6],
        "facility_quality": ratings[7],
        "total_user_rated": ratings[0],
        "is_user_rated": bool(is_user_rated)
    }
    return place_with_vote



@router.delete('/place/delete/{id}')
def delete_place(id:int, db: Session = Depends(get_db), current_user= Depends(get_current_user)):
    place = db.query(Place).filter(Place.id == id).first() # This always return some query, so it can't be empty.
    # .first() always return orm, if found and none if not found.
    role = current_user.role
    if role == 'admin':
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The place of the id:{id} is not found.')
        
        else:
            db.delete(place)
            db.commit()

            return {'success':'The place has been deleted.'}
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
@router.put('/place/update/{id}')
def update_place(request:AdminUpdatePlace, id:int, db: Session = Depends(get_db), current_user= Depends(get_current_user)):
    place_query = db.query(Place).filter(Place.id == id)
    place = place_query.first()
    role = current_user.role
    # print(role)
    if role == 'staff' or role == 'admin':
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The place of the id:{id} is not found.')
        
        place_query.update(request.model_dump(), synchronize_session=False)
        db.commit()

        return {'success':'post updated.'}
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")


# @router.get('/places/search/')
# def search_place(search:str = None, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
