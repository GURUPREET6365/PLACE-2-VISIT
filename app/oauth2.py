from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from app.database.pydantic_models import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.database.models import User
from google.oauth2 import id_token
from google.auth.transport import requests

# This is login, means this is the path where the dependency is for the token and passwordresetform, which is in login.
"""
Look for Authorization: Bearer <token> in request headers and extract <token>”
login is only indicates that you will get the token at login, that's it.

"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

"""
oauth2_scheme that we created forces to have token and for the places we don't want as for the unauthorized user we will directly give the place and for authorized, we will give their voting also...
"""
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl='login', auto_error=False)

load_dotenv()

"""
A JWT (JSON Web Token) consists of three base64url-encoded parts separated by dots (.): a Header, a Payload, and a Signature. The format is header.payload.signature, designed to be compact and secure for transmitting claims between parties. 

Header: Contains metadata about the token, typically the type of token (JWT) and the signing algorithm used (e.g., HMAC SHA256 or RSA).

Payload: Contains the claims, which are statements about an entity (usually user data) and additional data like expiration time (exp) and issuer (iss).

Signature: Created by hashing the encoded header, encoded payload, and a secret key, ensuring the token has not been tampered with. 
"""

# SECRET KEY
# Algorithm
# expiration time

SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7200

# For Google auth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')



def create_access_token(data:dict):
    # storing the data into variable for to not lost while processing or manipulating
    to_encode = data.copy()
    # print(to_encode)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})
    
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # print(jwt_token)
    return jwt_token


# credentials_exceptions is the error, when it will cause. This is done for the code reusability.
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # print(payload)
        # print(type(payload))
        """
        we can't use, id: str = payload['user_id'],
         because by chance if the token is not, this method will give error that will crash the server.

        """
        id: int = payload.get('user_id')
        email = payload.get('email')
        # This type of colon is used to show that we here id, will only accept the string.

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id, email=email)
    except JWTError:
        raise credentials_exception
    
    return token_data

"""
This token in get current user is given by the oauth2_scheme, as it is built in and from where the dependency of this fucntion is created, it will directly, take the token from Authorization: Bearer <token>
"""
def get_current_user(token:str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    # print('The token.id is', token.id)
    current_user = db.query(User).filter(User.id == token.id).first()

    if current_user is None:
        raise credentials_exception
    return current_user

# This is for the place and this will take the token if available and if not then it will not take.
def get_current_user_optional(token:str = Depends(oauth2_scheme_optional), db:Session = Depends(get_db)):
    if token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials',
            headers={"WWW-Authenticate": "Bearer"})
        user = verify_access_token(token, credentials_exception)
        current_user = db.query(User).filter(User.id == user.id).first()
        # .first used as it returns none if no data found
        if current_user:
            return current_user
        else:
            return None



# this is the token sent by the client, this will be verified and then data of the google logged in user will be extracted.
def google_token_verification(token, db: Session):
    # print('got token, now verifying...')
    # Extracting the information from the token given by google.
    request = requests.Request()
    try:
        # print('verifying token')
        token_info = id_token.verify_oauth2_token(token, request, GOOGLE_CLIENT_ID)
        
        """
        # print(token_info)
        {'iss': 'https://accounts.google.com', 'azp': '788471062927-m9k1jhqtp4j1gr2be8fg4bga08mi4knd.apps.googleusercontent.com', 'aud': '788471062927-m9k1jhqtp4j1gr2be8fg4bga08mi4knd.apps.googleusercontent.com', 'sub': '108517204962045586134', 'email': 'streakmanager001@gmail.com', 'email_verified': True, 'nbf': 1769369179, 'name': 'Streak Manager', 'picture': 'https://lh3.googleusercontent.com/a/ACg8ocLM1jRuZwyU5xY5GkrajnKtPm1WqjMJAjL7rd-hDR_pUj3vYw=s96-c', 'given_name': 'Streak', 'family_name': 'Manager', 'iat': 1769369479, 'exp': 1769373079, 'jti': '842407703ec41d076b926174dd1a2e7bcc446d84'}
        """

    except Exception:
        # print(error)
        # print('Token got wrong')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    sub = token_info["sub"]
    email = token_info["email"]
    first_name = token_info.get("given_name")
    last_name = token_info.get("family_name")
    profile_url = token_info.get("picture")

    user = db.query(User).filter(User.google_sub == sub).first()
    if user:
        # This is because something user changes their email.
        if email != user.email:
            user.email = email
            db.commit()
            jwt_access_token = create_access_token(data={'user_id':user.id, 'email':user.email})
            return jwt_access_token
        
        # If email is matched means the email will be same, user not updated their email.
        jwt_access_token = create_access_token(data={'user_id':user.id, 'email':user.email})
        return jwt_access_token

    # Now I am checking that user exists with their email or not?
    user_with_email = db.query(User).filter(User.email == email).first()
    if user_with_email:
        user_with_email.first_name = first_name
        user_with_email.last_name = last_name
        user_with_email.profile_url = profile_url
        # local_google is used for the suer that can log in with both local and google
        user_with_email.provider = 'local_google'
        user_with_email.google_sub = sub

        db.commit()

        jwt_access_token = create_access_token(data={'user_id': user_with_email.id, 'email': user_with_email.email})
        return jwt_access_token

    # If user is not exists then create new user.
    else:
        create_user=User(
            email=email, 
            first_name=first_name,
            google_sub=sub, 
            last_name=last_name,
            profile_url=profile_url,
            provider='google'
        )
        db.add(create_user)
        db.commit()
        db.refresh(create_user)

        jwt_access_token = create_access_token(data={'user_id':create_user.id, 'email':create_user.email})
        return jwt_access_token
        
