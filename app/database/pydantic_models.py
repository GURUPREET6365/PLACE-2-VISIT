from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# This is the pydantic validation model for the upcoming request for the Places.
class Places(BaseModel):
    place_name:str
    place_address:str
    about_place:str
    pincode:int
    user_id: Optional[int] = None


class responsePlace(Places):
    id:int
    created_at:datetime

    class Config:
        from_attributes = True


# users
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    first_name:str
    last_name:str

# This is the login model for taking the data from the staff....
class LoginUser(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_url: Optional[str] = None
    provider: Optional[str] = None
    role:str
    created_at:datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: int
    email: EmailStr

class GoogleAuthToken(BaseModel):
    token:str

class VoteRequest(BaseModel):
    vote: bool | None = None