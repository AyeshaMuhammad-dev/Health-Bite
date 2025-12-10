"""
Chatbot route for nutrition/fitness Q&A using OpenAI GPT-4.1.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.openai_service import OpenAIService

router = APIRouter()


class ChatbotQuery(BaseModel):
    """Chatbot query request model."""
    query: str
    user_context: dict = None


class ChatbotResponse(BaseModel):
    """Chatbot response model."""
    response: str
    query: str


@router.post("/query", response_model=ChatbotResponse)
async def chatbot_query(request: ChatbotQuery):
    """
    Handle chatbot queries about nutrition and fitness.
    
    Example:
    ```json
    {
        "query": "What are some healthy breakfast options?",
        "user_context": {
            "age": 30,
            "weight": 70,
            "goals": ["weight_loss"]
        }
    }
    ```
    """
    try:
        openai_service = OpenAIService()
        response_text = await openai_service.chat_completion(
            query=request.query,
            user_context=request.user_context
        )
        
        return ChatbotResponse(
            query=request.query,
            response=response_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chatbot query: {str(e)}"
        )
