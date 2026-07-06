from pydantic import BaseModel, EmailStr
from typing import Optional






class Token(BaseModel):
    is_token:bool
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: int
    email: EmailStr

class GoogleAuthToken(BaseModel):
    token:str

