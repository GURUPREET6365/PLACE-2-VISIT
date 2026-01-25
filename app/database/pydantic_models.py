from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# This is the pydantic validation model for the upcoming request for the Places.
class Places(BaseModel):
    place_name:str
    place_address:str
    pincode:int
    user_id:int

class responsePlace(Places):
    id:int
    created_at:datetime
    success: bool = True

    class Config:
        from_attributes = True


# users
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    first_name:str
    last_name:str


class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: int
    email: EmailStr