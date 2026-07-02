from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# users
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    first_name:str
    last_name:str


class UpdateUser(BaseModel):
    first_name:str
    last_name:str
    role: str



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

    model_config = {
        "from_attributes": True
    }
