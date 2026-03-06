from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will recieve from the client.
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.database.models import User
from app.utilities.utils import check_password
from app.oauth2 import create_access_token, google_token_verification
from app.database.pydantic_models import Token, GoogleAuthToken, LoginUser

router = APIRouter(
    prefix='/api',
    tags=['Authentication']
)

@router.post('/auth/google', response_model=Token)
def google_auth(request: GoogleAuthToken, db: Session = Depends(get_db)):
    access_token = google_token_verification(request.token, db)
    return {'access_token': access_token, 'token_type': 'bearer'}
