from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from typing import List
from sqlalchemy.orm import Session
from app.database.database import get_db
# This is the pydantic validation model
from app.routers.places.pydanticModels import Places
# This is the pydantic response model
from app.routers.places.pydanticModels import AllPlaceResponse, SpecificPlaceResponseModel
from app.routers.users.adminpanel.pydanticModels import AdminUpdatePlace
from app.database.models import Place, Votes, Ratings
from app.utilities.oauth2 import get_current_user, get_current_user_optional
from sqlalchemy import and_
from app.routers.places.helper_function import all_place_response, search_place_endpoint
from app.routers.places.db_ops import PlacesDbOps
from app.routers.places.helper_function import specific_place_response

# models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix='/api',
    tags=['Place']
)

# this is the db ops initializer which will initialize the class.
def db_ops_init(db: Session = Depends(get_db)):
    return PlacesDbOps(db)


# This is returning a list so we need to use List from typing library.
@router.get('/all/place', status_code=status.HTTP_200_OK, response_model=List[AllPlaceResponse])
def all_place(db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user_optional)):

    # Finding average rating of overall categories
    place = all_place_response(current_user, db_ops)
    return place

"""
Depends is the function which tells that first run and give me the result then run next function.
"""

@router.post('/add/place', status_code=status.HTTP_201_CREATED)
def create_place(request: Places, db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    # print(request.model_dump())
    # This is going to first convert into dict and then unpack it.

    # Checking that the place_name or place
    role = current_user.role
    if role == 'staff' or role == 'admin':
        if db_ops.create_place(request):
            return {"message":"place created successfully"}
        
        raise HTTPException(status_code=status.WS_1005_NO_STATUS_RCVD, detail="Error!")

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

@router.get('/place/{id}', response_model=SpecificPlaceResponseModel)
def specific_place(id: int, db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    user_id = current_user.id
    place_id=id
    place_with_vote = specific_place_response(db_ops, user_id, place_id)
    return place_with_vote

@router.delete('/place/delete/{id}')
def delete_place(id:int, db_ops: Session = Depends(db_ops_init), current_user= Depends(get_current_user)):
    place = db_ops.place_query_with_id(id)   # This always return some query, so it can't be empty.
    # .first() always return orm, if found and none if not found.
    role = current_user.role
    if role == 'admin':
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The place of the id:{id} is not found.')
        
        else:
            db_ops.delete_query(place)
            return {'success':'The place has been deleted.'}
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
@router.put('/place/update/{id}')
def update_place(request:AdminUpdatePlace, id:int, db_ops: Session = Depends(db_ops_init), current_user= Depends(get_current_user)):
    db=db_ops.get_only_db()
    place_query = db.query(Place).filter(Place.id == id)
    place = place_query.first()
    role = current_user.role
    # print(role)
    if role == 'staff' or role == 'admin':
        if not place:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The place of the id:{id} is not found.')
        
        db_ops.update_query(place_query, request)

        return {'success':'post updated.'}
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")


@router.get('/places/search/', response_model=List[AllPlaceResponse])
def search_place(
    search,
    db_ops: Session = Depends(db_ops_init),
    current_user = Depends(get_current_user_optional)):

    # print(current_user)
    return search_place_endpoint(current_user, db_ops, search)
