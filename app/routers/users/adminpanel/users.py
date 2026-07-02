from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from app.utilities.oauth2 import get_current_user
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import User
from app.routers.users.adminpanel.pydanticModels import AdminUserResponse
from typing import List
from sqlalchemy import String, or_, cast

router = APIRouter(
    prefix='/api/admin',
    tags=['admin/staff panel']
)


@router.get('/user', response_model=List[AdminUserResponse])
def admin_user(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin':
        user = db.query(User).all()
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')




@router.get('/user/search', response_model=List[AdminUserResponse])
def admin_search_user(search, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin':
        user = []

        search_query = search.split()

        for query in search_query:
            search_pattern= f"%{query}%"
            user_search = db.query(User).filter(
                or_(User.first_name.ilike(search_pattern), (User.last_name.ilike(search_pattern)),
                    (User.email.ilike(search_pattern)),
                    (cast(User.google_sub, String).ilike(search_pattern)))).limit(20).all()

            user.extend(user_search)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')



