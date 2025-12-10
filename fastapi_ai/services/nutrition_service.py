"""
Nutrition service for food analysis using Nutritionix/Edamam APIs.
"""
import os
import httpx
from typing import Dict, Any


class NutritionService:
    """Service for food nutrition analysis."""
    
    def __init__(self):
        self.nutritionix_app_id = os.getenv('NUTRITIONIX_APP_ID')
        self.nutritionix_api_key = os.getenv('NUTRITIONIX_API_KEY')
        self.edamam_app_id = os.getenv('EDAMAM_APP_ID')
        self.edamam_app_key = os.getenv('EDAMAM_APP_KEY')
    
    async def analyze_food(self, food_name: str) -> Dict[str, Any]:
        """
        Analyze food nutrition using Nutritionix or Edamam API.
        
        Args:
            food_name: Name of the food item
            
        Returns:
            Dictionary with calories, nutrients, and serving size
        """
        # Try Nutritionix first, fallback to Edamam, then to estimate
        if self.nutritionix_app_id and self.nutritionix_api_key:
            try:
                return await self._analyze_with_nutritionix(food_name)
            except Exception:
                pass
        
        if self.edamam_app_id and self.edamam_app_key:
            try:
                return await self._analyze_with_edamam(food_name)
            except Exception:
                pass
        
        # Fallback to estimation if APIs are not available
        return self._estimate_nutrition(food_name)
    
    async def _analyze_with_nutritionix(self, food_name: str) -> Dict[str, Any]:
        """Analyze food using Nutritionix API."""
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "x-app-id": self.nutritionix_app_id,
            "x-app-key": self.nutritionix_api_key,
            "Content-Type": "application/json",
        }
        data = {"query": food_name}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            foods = result.get('foods', [])
            if foods:
                food = foods[0]
                return {
                    "name": food.get('food_name', food_name),
                    "calories": food.get('nf_calories', 0),
                    "nutrients": {
                        "protein": food.get('nf_protein', 0),
                        "carbs": food.get('nf_total_carbohydrate', 0),
                        "fats": food.get('nf_total_fat', 0),
                        "fiber": food.get('nf_dietary_fiber', 0),
                        "sugar": food.get('nf_sugars', 0),
                    },
                    "serving_size": food.get('serving_unit', '1 serving'),
                }
        
        raise Exception("No nutrition data found")
    
    async def _analyze_with_edamam(self, food_name: str) -> Dict[str, Any]:
        """Analyze food using Edamam API."""
        url = "https://api.edamam.com/api/nutrition-data"
        params = {
            "app_id": self.edamam_app_id,
            "app_key": self.edamam_app_key,
            "ingr": food_name,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            calories = result.get('calories', 0)
            total_nutrients = result.get('totalNutrients', {})
            
            return {
                "name": food_name,
                "calories": calories,
                "nutrients": {
                    "protein": total_nutrients.get('PROCNT', {}).get('quantity', 0),
                    "carbs": total_nutrients.get('CHOCDF', {}).get('quantity', 0),
                    "fats": total_nutrients.get('FAT', {}).get('quantity', 0),
                    "fiber": total_nutrients.get('FIBTG', {}).get('quantity', 0),
                    "sugar": total_nutrients.get('SUGAR', {}).get('quantity', 0),
                },
                "serving_size": "100g",
            }
    
    def _estimate_nutrition(self, food_name: str) -> Dict[str, Any]:
        """
        Estimate nutrition values when APIs are unavailable.
        This is a simple fallback - in production, use proper APIs.
        """
        food_name_lower = food_name.lower()
        
        # Simple estimation logic based on common foods
        estimates = {
            'chicken': {'calories': 231, 'protein': 43.5, 'carbs': 0, 'fats': 5},
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fats': 0.3},
            'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fats': 0.2},
            'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fats': 0.3},
            'egg': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fats': 11},
        }
        
        # Try to match food name
        matched = None
        for key, values in estimates.items():
            if key in food_name_lower:
                matched = values
                break
        
        if not matched:
            # Default estimation
            matched = {'calories': 150, 'protein': 10, 'carbs': 15, 'fats': 5}
        
        return {
            "name": food_name,
            "calories": matched['calories'],
            "nutrients": {
                "protein": matched['protein'],
                "carbs": matched['carbs'],
                "fats": matched['fats'],
                "fiber": 2.0,
                "sugar": 5.0,
            },
            "serving_size": "100g (estimated)",
        }
