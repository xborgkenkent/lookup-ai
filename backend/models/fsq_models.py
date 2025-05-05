from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class Parking(BaseModel):
    parking: Optional[Union[Dict, bool]] = None
    street_parking: Optional[Union[Dict, bool]] = None
    valet_parking: Optional[Union[Dict, bool]] = None
    public_lot: Optional[Union[Dict, bool]] = None
    private_lot: Optional[Union[Dict, bool]] = None

class Amenities(BaseModel):
    restroom: Optional[Union[Dict, bool]] = None
    smoking: Optional[Union[Dict, bool]] = None
    jukebox: Optional[Union[Dict, bool]] = None
    music: Optional[Union[Dict, bool]] = None
    live_music: Optional[Union[Dict, bool]] = None
    private_room: Optional[Union[Dict, bool]] = None
    outdoor_seating: Optional[Union[Dict, bool]] = None
    tvs: Optional[Union[Dict, bool]] = None
    atm: Optional[Union[Dict, bool]] = None
    coat_check: Optional[Union[Dict, bool]] = None
    wheelchair_accessible: Optional[Union[Dict, bool]] = None
    parking: Optional[Parking] = None
    sit_down_dining: Optional[Union[Dict, bool]] = None
    wifi: Optional[Union[str, bool]] = None

class Features(BaseModel):
    amenities: Optional[Amenities] = None

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
    features: Optional[Features] = None
    hours: Optional[FourSquareHours] = None
    location: FourSquareLocation
    menu: Optional[str] = None
    name: str
    price: Optional[int] = None
    rating: Optional[float] = None

class FourSquareResponse(BaseModel):
    results: List[FourSquareResult]