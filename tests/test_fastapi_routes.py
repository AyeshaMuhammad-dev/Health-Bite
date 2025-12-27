"""
Unit tests for FastAPI routes.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'fastapi_ai'))

from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Health-Bite AI Services API" in response.json()["message"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@patch('fastapi_ai.routes.chatbot.OpenAIService')
def test_chatbot_query(mock_openai_service):
    """Test chatbot query endpoint."""
    mock_service_instance = mock_openai_service.return_value
    mock_service_instance.chat_completion = AsyncMock(return_value="Eat more vegetables!")
    
    response = client.post(
        "/chatbot/query",
        json={"query": "What should I eat for breakfast?"}
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["query"] == "What should I eat for breakfast?"


@patch('fastapi_ai.routes.diet.OpenAIService')
def test_generate_diet_plan(mock_openai_service):
    """Test diet plan generation endpoint."""
    mock_service_instance = mock_openai_service.return_value
    mock_service_instance.generate_diet_plan = AsyncMock(return_value={
        "daily_calorie_target": 2000,
        "weekly_plan": {}
    })
    
    response = client.post(
        "/diet/generate",
        json={
            "age": 30,
            "gender": "male",
            "height": 175,
            "weight": 80
        }
    )
    
    assert response.status_code == 200
    assert "plan" in response.json()


@patch('fastapi_ai.routes.food.NutritionService')
def test_analyze_food(mock_nutrition_service):
    """Test food analysis endpoint."""
    mock_service_instance = mock_nutrition_service.return_value
    mock_service_instance.analyze_food = AsyncMock(return_value={
        "name": "Chicken Breast",
        "calories": 231,
        "nutrients": {"protein": 43.5, "carbs": 0, "fats": 5}
    })
    
    response = client.post(
        "/food/analyze",
        json={"name": "Chicken Breast"}
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Chicken Breast"
    assert "calories" in response.json()


@patch('fastapi_ai.routes.restaurant.MapsService')
def test_nearby_restaurants(mock_maps_service):
    """Test nearby restaurants endpoint."""
    mock_service_instance = mock_maps_service.return_value
    mock_service_instance.find_healthy_restaurants = AsyncMock(return_value=[
        {
            "name": "Green Leaf Cafe",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
            "healthy_options": ["Salad", "Grilled Chicken"]
        }
    ])
    
    response = client.get(
        "/restaurant/nearby",
        params={"latitude": 40.7128, "longitude": -74.0060}
    )
    
    assert response.status_code == 200
    assert "restaurants" in response.json()
    assert len(response.json()["restaurants"]) > 0
