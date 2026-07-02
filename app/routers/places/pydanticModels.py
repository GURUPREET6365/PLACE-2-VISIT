from pydantic import BaseModel
from datetime import datetime




# This is the pydantic validation model for the upcoming request for the Places.
class Places(BaseModel):
    place_name:str
    place_address:str
    about_place:str
    pincode:int
    user_id: int


class AllPlaceResponse(BaseModel):
    place_name:str
    place_address:str
    about_place:str
    pincode:int
    id:int
    voted:bool | None = None
    created_at: datetime
    num_likes: int
    num_dislikes: int
    overall: float
    total_user_rated:int
    is_user_rated: bool | None = None

    model_config = {
        "from_attributes": True
    }




class SpecificPlaceResponseModel(AllPlaceResponse):
    overall:float
    cleanliness:float
    safety:float
    crowd_behavior:float
    lightning:float
    transport_access:float
    facility_quality:float

    model_config = {
        "from_attributes": True
    }




