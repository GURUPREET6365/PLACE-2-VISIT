from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will recieve from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
from app.utilities.oauth2 import google_token_verification
from app.database.pydantic_models import Token, GoogleAuthToken

router = APIRouter(
    prefix="/api",
    tags=['Authentication']
)

@router.post('/auth/google', response_model=Token)
def google_auth(request: GoogleAuthToken, db: Session = Depends(get_db)):
    is_token, access_token = google_token_verification(request.token, db)
    if is_token:
        return {'is_token':is_token,'access_token': access_token, 'token_type': 'bearer'}
    
    return {'is_token':is_token,'access_token': access_token, 'token_type':'Invalid'}
        
