from fastapi import Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from app.utilities.oauth2 import get_current_user
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.routers.users.adminpanel.pydanticModels import AdminPlaceResponse
from typing import List
from app.routers.users.adminpanel.db_ops import AdminPanelDbOps
from app.routers.users.adminpanel.helper_function import (
    admin_place_response,
    admin_search_place_response,
)

# creating fastapi router for endpoint
router = APIRouter(
    prefix='/api/admin',
    tags=['admin/staff panel']
)


def db_ops_init(db: Session = Depends(get_db)):
    return AdminPanelDbOps(db)


# This is the endpoint for staff/admin where he can only add the place and edit the place.
@router.get('/place', response_model=List[AdminPlaceResponse])
def admin_place(db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    return admin_place_response(db_ops, current_user)

# This is admin place search
@router.get('/place/search', response_model=List[AdminPlaceResponse])
def admin_search_place(search, db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    return admin_search_place_response(search, db_ops, current_user)
