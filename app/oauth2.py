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


# This is login, means this is the path where the dependency is for the token and passwordresetform, which is in login.
"""
Look for Authorization: Bearer <token> in request headers and extract <token>”
login is only indicates that you will get the token at login, that's it.

"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

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
ACCESS_TOKEN_EXPIRE_MINUTES = 720


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

    return current_user