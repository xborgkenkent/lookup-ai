import os
import logging
import httpx
from fastapi import HTTPException
from typing import List
from dotenv import load_dotenv
from utils.constants import restaurant_fields, categories
from models.restaurant_models import RestaurantResponse
from models.fsq_models import FourSquareResponse, FourSquareResult

load_dotenv()
logger = logging.getLogger(__name__)

FSQ_API_KEY = os.environ.get("FSQ_API_KEY")
FSQ_BASE_URL = os.environ.get("FSQ_BASE_URL")
if not FSQ_API_KEY:
    logger.critical("FSQ_API_KEY environment variable is not set")
    raise RuntimeError("FSQ_API_KEY environment variable is not set")

if not FSQ_BASE_URL:
    logger.critical("FSQ_BASE_URL environment variable is not set")
    raise RuntimeError("FSQ_BASE_URL environment variable is not set")

async def fsq_search(action: str, parameters: dict) -> List[RestaurantResponse]:
    try:
        if not parameters:
            raise HTTPException(status_code=400, detail="No search parameters provided.")
    
        categoryIds = [categories.get(action)] or categories.values()
        
        parameters["fields"] = ",".join(restaurant_fields)
        parameters["categories"] = ",".join([str(category) for category in categoryIds])
        
        query_string = "&".join([f"{key}={value}" for key, value in parameters.items()])
        
        url = f"{FSQ_BASE_URL}?{query_string}"
        headers = {
            "Accept": "application/json",
            "Authorization": FSQ_API_KEY
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from Foursquare API.")
        
        data = FourSquareResponse.model_validate(response.json())
        
        return get_restaurants(data.results)
    
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(status_code=502, detail=f"Request error: {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e}")

def get_restaurants(restaurants: List[FourSquareResult]):
    """Extract restaurant details from the Foursquare results."""
    restaurant_list = []
    
    try:
        for restaurant in restaurants:
            formatted = format_location(restaurant.location)
            
            hours_display = None
            if restaurant.hours:
                hours_display = restaurant.hours.display
            
            restaurant_summary = RestaurantResponse(
                name=restaurant.name,
                address=formatted,
                fsq_id=restaurant.fsq_id,
                hours=hours_display,
                rating=restaurant.rating,
                price=restaurant.price,
                cuisine=restaurant.menu
            )
            restaurant_list.append(restaurant_summary)
        
        return restaurant_list
    except Exception as e:
        logger.error(f"Error processing restaurant data: {e}")

def format_location(location):
    """
    Format the location for display.
    There's a chance that the location is not formatted, so we need to create a custom format.
    """
    formatted = location.formatted_address or ""
    
    if not formatted:
        addr = location.address or ""
        cross = location.cross_street or ""
        locality = location.locality or ""
        region = location.region or ""
        postcode = location.postcode or ""

        formatted = f"{addr} ({cross}), {locality}, {region} {postcode}".strip()
        formatted = formatted.replace(" ()", "").replace(" ,", ",").strip()
    
    return formatted