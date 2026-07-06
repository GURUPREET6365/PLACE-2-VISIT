from fastapi import Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from app.utilities.oauth2 import get_current_user
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.routers.users.adminpanel.pydanticModels import AdminUserResponse
from typing import List
from app.routers.users.adminpanel.db_ops import AdminPanelDbOps
from app.routers.users.adminpanel.helper_function import (
    admin_search_user_response,
    admin_user_response,
)

router = APIRouter(
    prefix='/api/admin',
    tags=['admin/staff panel']
)


def db_ops_init(db: Session = Depends(get_db)):
    return AdminPanelDbOps(db)


@router.get('/user', response_model=List[AdminUserResponse])
def admin_user(db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    return admin_user_response(db_ops, current_user)




@router.get('/user/search', response_model=List[AdminUserResponse])
def admin_search_user(search, db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    return admin_search_user_response(search, db_ops, current_user)



