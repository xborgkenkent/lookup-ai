from pydantic import BaseModel
from typing import Optional, List

class FourSquareRegular(BaseModel):
    close: str
    day: int
    open: str

class FourSquareHours(BaseModel):
    display: Optional[str] = None
    is_local_holiday: Optional[bool] = None
    open_now: Optional[bool] = None
    regular: Optional[List[FourSquareRegular]] = None

class FourSquareLocation(BaseModel):
    address: Optional[str] = None
    address_extended: Optional[str] = None
    admin_region: Optional[str] = None
    census_block: Optional[str] = None
    country: Optional[str] = None
    cross_street: Optional[str] = None
    dma: Optional[str] = None
    formatted_address: Optional[str] = None
    locality: Optional[str] = None
    neighborhood: Optional[List[str]] = None
    po_box: Optional[str] = None
    post_town: Optional[str] = None
    postcode: Optional[str] = None
    region: Optional[str] = None

class FourSquareResult(BaseModel):
    fsq_id: str
    hours: Optional[FourSquareHours] = None
    location: FourSquareLocation
    menu: Optional[str] = None
    name: str
    price: Optional[int] = None
    rating: Optional[float] = None

class FourSquareResponse(BaseModel):
    results: List[FourSquareResult]