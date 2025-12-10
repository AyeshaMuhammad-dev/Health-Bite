"""
Google Maps service for finding healthy restaurants.
"""
import os
import httpx
from typing import List, Dict, Any


class MapsService:
    """Service for Google Maps API interactions."""
    
    def __init__(self):
        self.google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.places_api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        self.details_api_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    async def find_healthy_restaurants(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """
        Find nearby healthy restaurants using Google Maps API.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in meters
            
        Returns:
            List of restaurant dictionaries with healthy options
        """
        if not self.google_maps_api_key:
            # Return mock data if API key is not available
            return self._get_mock_restaurants(latitude, longitude)
        
        try:
            # Search for restaurants
            restaurants = await self._search_restaurants(latitude, longitude, radius)
            
            # Filter and enhance with healthy options
            healthy_restaurants = []
            for restaurant in restaurants:
                healthy_options = await self._identify_healthy_options(restaurant)
                if healthy_options:  # Only include restaurants with healthy options
                    restaurant['healthy_options'] = healthy_options
                    healthy_restaurants.append(restaurant)
            
            return healthy_restaurants[:20]  # Limit to 20 results
        except Exception as e:
            # Fallback to mock data on error
            print(f"Error fetching restaurants: {e}")
            return self._get_mock_restaurants(latitude, longitude)
    
    async def _search_restaurants(
        self,
        latitude: float,
        longitude: float,
        radius: int
    ) -> List[Dict[str, Any]]:
        """Search for restaurants using Google Places API."""
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "type": "restaurant",
            "keyword": "healthy food",
            "key": self.google_maps_api_key,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.places_api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            restaurants = []
            for place in data.get('results', [])[:20]:
                restaurant = {
                    "place_id": place.get('place_id'),
                    "name": place.get('name'),
                    "rating": place.get('rating'),
                    "price_level": place.get('price_level'),
                    "location": {
                        "latitude": place['geometry']['location']['lat'],
                        "longitude": place['geometry']['location']['lng'],
                    },
                    "address": place.get('vicinity', ''),
                }
                
                # Get more details
                details = await self._get_place_details(place.get('place_id'))
                if details:
                    restaurant.update(details)
                
                restaurants.append(restaurant)
            
            return restaurants
    
    async def _get_place_details(self, place_id: str) -> Dict[str, Any]:
        """Get detailed information about a place."""
        params = {
            "place_id": place_id,
            "fields": "formatted_phone_number,website,opening_hours",
            "key": self.google_maps_api_key,
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.details_api_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                result = data.get('result', {})
                return {
                    "phone": result.get('formatted_phone_number', ''),
                    "website": result.get('website', ''),
                    "opening_hours": result.get('opening_hours', {}).get('weekday_text', []),
                }
        except Exception:
            return {}
    
    async def _identify_healthy_options(self, restaurant: Dict[str, Any]) -> List[str]:
        """
        Identify healthy menu options for a restaurant.
        In a real implementation, this would use restaurant menu APIs or web scraping.
        """
        # Common healthy keywords
        healthy_keywords = [
            "grilled", "steamed", "salad", "vegetable", "fruit",
            "whole grain", "lean protein", "organic", "fresh",
            "low-fat", "low-calorie", "plant-based", "vegan", "vegetarian"
        ]
        
        # For now, return generic healthy options based on restaurant type
        # In production, integrate with menu APIs or use AI to analyze menus
        return [
            "Grilled Chicken Salad",
            "Quinoa Bowl with Vegetables",
            "Fresh Fruit Smoothie",
            "Steamed Vegetables with Brown Rice",
            "Lean Protein Options"
        ]
    
    def _get_mock_restaurants(
        self,
        latitude: float,
        longitude: float
    ) -> List[Dict[str, Any]]:
        """Return mock restaurant data when API is unavailable."""
        return [
            {
                "name": "Green Leaf Cafe",
                "location": {
                    "latitude": latitude + 0.01,
                    "longitude": longitude + 0.01,
                },
                "address": "123 Healthy Street",
                "rating": 4.5,
                "price_level": 2,
                "healthy_options": [
                    "Organic Kale Salad",
                    "Grilled Salmon Bowl",
                    "Fresh Juice Bar"
                ],
            },
            {
                "name": "Fit Kitchen",
                "location": {
                    "latitude": latitude - 0.01,
                    "longitude": longitude + 0.02,
                },
                "address": "456 Fitness Avenue",
                "rating": 4.7,
                "price_level": 3,
                "healthy_options": [
                    "Protein Power Bowl",
                    "Quinoa & Vegetable Mix",
                    "Green Smoothie"
                ],
            },
        ]
