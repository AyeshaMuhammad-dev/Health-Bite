"""
Diet plan generation route using OpenAI GPT-4.1.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ..services.openai_service import OpenAIService

router = APIRouter()


class DietPlanRequest(BaseModel):
    """Diet plan generation request model."""
    age: int = None
    gender: str = None
    height: float = None
    weight: float = None
    goals: Dict[str, Any] = None


class DietPlanResponse(BaseModel):
    """Diet plan response model."""
    plan: Dict[str, Any]
    message: str


@router.post("/generate", response_model=DietPlanResponse)
async def generate_diet_plan(user_profile: DietPlanRequest):
    """
    Generate personalized diet plan using AI.
    
    Example:
    ```json
    {
        "age": 30,
        "gender": "male",
        "height": 175,
        "weight": 80,
        "goals": {
            "weight_loss": true,
            "muscle_gain": false
        }
    }
    ```
    """
    try:
        openai_service = OpenAIService()
        plan = await openai_service.generate_diet_plan(user_profile.dict())
        
        return DietPlanResponse(
            plan=plan,
            message="Diet plan generated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating diet plan: {str(e)}"
        )
