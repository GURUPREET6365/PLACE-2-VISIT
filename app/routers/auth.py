from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will recieve from the client.
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import User
from app.utilities.utils import check_password
from app.oauth2 import create_access_token, google_token_verification
from app.database.pydantic_models import Token, GoogleAuthToken

router = APIRouter(
    prefix='/api', 
    tags=['Authentication']
)

# NOTE: The login api will recieve the form data not the json data.

@router.post('/login', response_model=Token)
def login(user_cred:OAuth2PasswordRequestForm=Depends() ,db: Session = Depends(get_db)):

    """
    OAuth2PasswordRequestForm:
    This is used because it will take the username and password as formadata not json.
    username field can be a email, but the name should be email
    """

    user = db.query(User).filter(User.email == user_cred.username).first()
    if not user:
        # print('user is not known')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    # print('mathcing password')
    is_match_pwd = check_password(user_cred.password, user.password)
    if not is_match_pwd:
        # print('password did not match')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    access_token = create_access_token(data={'user_id':user.id, 'email':user.email})
    
    return {'access_token':access_token, 'token_type':'bearer'}


@router.post('/auth/google', response_model=Token)
def google_auth(request:GoogleAuthToken, db: Session = Depends(get_db)):
    access_token = google_token_verification(request.token, db)
    
    return {'access_token':access_token, 'token_type':'bearer'}