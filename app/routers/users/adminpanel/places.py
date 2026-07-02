from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from app.utilities.oauth2 import get_current_user
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.routers.users.adminpanel.pydanticModels import AdminPlaceResponse
# This place is for admin panel so it will respond everything and that's why, I respond with the same model that I used to create
from app.database.models import Place
from typing import List
from sqlalchemy import String, or_, cast

# creating fastapi router for endpoint
router = APIRouter(
    prefix='/api/admin',
    tags=['admin/staff panel']
)


# This is the endpoint for staff/admin where he can only add the place and edit the place.
@router.get('/place', response_model=List[AdminPlaceResponse])
def admin_place(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin' or role=='staff':
        place = db.query(Place).all()
        return place

#     if not staff and admin and also tried to access
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')

# This is admin place search
@router.get('/place/search', response_model=List[AdminPlaceResponse])
def admin_search_place(search, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin' or role=='staff':
        search_query = search.split()
        place = []
        for all_query in search_query:
            search_pattern = f"%{all_query}%"
            place_search = db.query(Place).filter(
                or_(Place.place_name.ilike(search_pattern), (Place.about_place.ilike(search_pattern)),
                    (Place.place_address.ilike(search_pattern)),
                    (cast(Place.pincode, String).ilike(search_pattern)))).limit(20).all()

            place.extend(place_search)

        return place
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')
