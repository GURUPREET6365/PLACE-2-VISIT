
from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from app.oauth2 import get_current_user
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import User
from app.utilities.utils import check_password
from app.oauth2 import create_access_token
from app.database.pydantic_models import LoginUser
from app.database.pydantic_models import AdminPlaceResponse
# This place is for admin panel so it will response everything and that's why, I response with the same model that I used to create
from app.database.models import Place
from typing import List

# creating fastapi router for endpoint
router = APIRouter(
    prefix='/api',
    tags=['admin/staff panel']
)

# This is login endpoint.
@router.post('/login')
def login(user_cred: LoginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_cred.email).first()

    # Verifying that is user exists or not, if exists then login and if not then send response that user is not registered.
    if not user:
        # print('user is not known')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    # print('matching password')
    if user.role == 'staff' or user.role == 'admin':

        is_match_pwd = check_password(user_cred.password, str(user.password))

        # Checking that the password matches or not.
        if not is_match_pwd:
            # print('password did not match')
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

        # if password matches then it will create the jwt token.
        access_token = create_access_token(data={'user_id': user.id, 'email': user.email})
        return {"token":access_token}

#     if login user is not the staff or admin then it will not log into
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorized User')

# This is the endpoint for staff/admin where he can only add the place and edit the place.
@router.get('/admin/place', response_model=List[AdminPlaceResponse])
def admin_place(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role
    if role == 'admin' or role=='staff':
        place = db.query(Place).all()
        return place

#     if not staff and admin and also tried to access
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')

