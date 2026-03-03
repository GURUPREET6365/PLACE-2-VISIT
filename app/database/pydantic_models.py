from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# This is the pydantic validation model for the upcoming request for the Places.
class Places(BaseModel):
    place_name:str
    place_address:str
    about_place:str
    pincode:int
    user_id: int

# This is for the place update request model by the admin/staff
class AdminUpdatePlace(BaseModel):
    place_name:str
    place_address:str
    about_place:str
    pincode:int


# This model is for the admin/staff response.
class AdminPlaceResponse(Places):
    id:int
    class Config:
        orm_mode = True
# Here orm_mode is true because when i am taking all the place from db, and direct sending as a list using pydantic, pydantic need to confirm that I can use orm to extract data.


class AllPlaceResponse(BaseModel):
    place_name:str
    place_address:str
    about_place:str
    pincode:int
    id:int
    voted:bool | None = None
    created_at: datetime

    class Config:
        from_attributes = True

# users
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    first_name:str
    last_name:str

# This is the model for response the user data
class AdminUserResponse(BaseModel):
    id:int
    email: EmailStr
    password: Optional[str] = None
    first_name: str
    last_name: str
    provider:Optional[str] = None
    google_sub:Optional[str] = None
    profile_url:Optional[str] = None
    role:str
    created_at:datetime

    class Config:
        orm_mode = True

# This is the login model for taking the data from the staff....
class LoginUser(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    role:str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_url: Optional[str] = None
    provider: Optional[str] = None
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

# This is for the response of the all votes with user and place
class AdminVoteResponse(BaseModel):
    id:int
    vote:bool | None = None
    user_id: int
    place_id: int
    voted_at: datetime