from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.routers.places.pydanticModels import Places
from app.database.pydantic_models import FeedbackRequest, RatingsRequest



# This is for the place update request model by the admin/staff
class AdminUpdatePlace(BaseModel):
    place_name:str
    place_address:str
    about_place:str
    pincode:int


# This model is for the admin/staff response.
class AdminPlaceResponse(Places):
    id:int

    model_config = {
        "from_attributes": True
    }
# Here orm_mode is true because when i am taking all the place from db, and direct sending as a list using pydantic, pydantic need to confirm that I can use orm to extract data.



# This is for the response of the all votes with user and place
class AdminVoteResponse(BaseModel):
    id:int
    vote:bool | None = None
    user_id: int
    place_id: int
    voted_at: datetime


class AdminFeedbackResponse(FeedbackRequest):
    id:int
    model_config = {
        "from_attributes": True
    }


class AdminRatingsResponse(RatingsRequest):
    id:int



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

    model_config = {
        "from_attributes": True
    }
