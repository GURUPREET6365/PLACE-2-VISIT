
from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will receive from the client.
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import User
from app.utilities.utils import check_password
from app.oauth2 import create_access_token
from app.database.pydantic_models import Token, LoginUser

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
