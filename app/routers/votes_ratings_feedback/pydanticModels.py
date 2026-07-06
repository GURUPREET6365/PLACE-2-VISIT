from pydantic import BaseModel, EmailStr
from typing import Optional


class VoteRequest(BaseModel):
    vote: bool | None = None



class RatingsRequest(BaseModel):
    user_id:Optional[int] = None
    place_id:Optional[int] = None
    overall:int
    cleanliness:int
    safety:int
    crowd_behavior:int
    lightning:int
    transport_access:int
    facility_quality:int



class FeedbackRequest(BaseModel):
    email:EmailStr
    name:str
    found_place:Optional[bool] = False
    message:str

