"""
Restaurant filtering route using Google Maps API.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ..services.maps_service import MapsService

router = APIRouter()


class RestaurantResponse(BaseModel):
    """Restaurant response model."""
    restaurants: List[Dict[str, Any]]


@router.get("/nearby", response_model=RestaurantResponse)
async def get_nearby_restaurants(
    latitude: float,
    longitude: float,
    radius: int = 5000
):
    """
    Get nearby healthy restaurants filtered by healthy options.
    
    Parameters:
    - latitude: Latitude coordinate
    - longitude: Longitude coordinate
    - radius: Search radius in meters (default: 5000)
    
    Example:
    ```
    GET /restaurant/nearby?latitude=40.7128&longitude=-74.0060&radius=5000
    ```
    """
    try:
        maps_service = MapsService()
        restaurants = await maps_service.find_healthy_restaurants(
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
        
        return RestaurantResponse(restaurants=restaurants)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding restaurants: {str(e)}"
        )
