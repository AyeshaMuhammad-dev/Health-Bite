"""
Food analysis route using Nutritionix/Edamam API.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ..services.nutrition_service import NutritionService

router = APIRouter()


class FoodAnalysisRequest(BaseModel):
    """Food analysis request model."""
    name: str


class FoodAnalysisResponse(BaseModel):
    """Food analysis response model."""
    name: str
    calories: float
    nutrients: Dict[str, Any]
    serving_size: str = None


@router.post("/analyze", response_model=FoodAnalysisResponse)
async def analyze_food(request: FoodAnalysisRequest):
    """
    Analyze food nutrition and estimate calories.
    
    Example:
    ```json
    {
        "name": "Grilled Chicken Breast"
    }
    ```
    """
    if not request.name:
        raise HTTPException(
            status_code=400,
            detail="Food name is required"
        )
    
    try:
        nutrition_service = NutritionService()
        analysis = await nutrition_service.analyze_food(request.name)
        
        return FoodAnalysisResponse(**analysis)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing food: {str(e)}"
        )
