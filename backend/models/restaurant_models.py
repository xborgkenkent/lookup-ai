from pydantic import BaseModel
from typing import Optional
 
class RestaurantResponse(BaseModel):
    name: str
    rating: Optional[float] = None
    price: Optional[float] = None
    hours: Optional[str] = None
    address: Optional[str] = None
    cuisine: Optional[str] = None
    fsq_id: str
    type: str = "restaurant"
    