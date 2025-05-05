from pydantic import BaseModel
from typing import Optional
from models.fsq_models import Features

class HotelResponse(BaseModel):
    name: str
    rating: Optional[float] = None
    price: Optional[float] = None
    hours: Optional[str] = None
    address: Optional[str] = None
    features: Optional[Features] = None
    fsq_id: str
    type: str = "hotel"