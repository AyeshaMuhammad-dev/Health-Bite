# Health-Bite API Endpoints Documentation

## Base URLs
- **Django REST API**: `http://localhost:8000/api/`
- **FastAPI AI Services**: `http://localhost:8001/`

## Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Django REST Framework Endpoints

### Authentication Endpoints

#### 1. Register User
**POST** `/api/auth/register/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "Ayesha",
  "password": "securepassword123",
  "password2": "securepassword123",
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

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "height": 175.0,
    "weight": 80.0,
    "goals": {
      "weight_loss": true,
      "muscle_gain": false
    },
    "date_joined": "2024-01-15T10:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

#### 2. Login
**POST** `/api/auth/login/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    ...
  },
  "tokens": {
    "refresh": "...",
    "access": "..."
  }
}
```

#### 3. Refresh Token
**POST** `/api/auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Profile Endpoints

#### 4. Get/Update Profile
**GET/PUT/PATCH** `/api/profile/`

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "age": 30,
  "gender": "male",
  "height": 175.0,
  "weight": 80.0,
  "goals": {...},
  "date_joined": "2024-01-15T10:30:00Z"
}
```

---

### Food Logging Endpoints

#### 5. List Food Entries
**GET** `/api/foods/`

**Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": "user@example.com",
      "name": "Grilled Chicken Breast",
      "calories": 231.0,
      "nutrients": {
        "protein": 43.5,
        "carbs": 0,
        "fats": 5.0
      },
      "logged_at": "2024-01-15T12:00:00Z"
    }
  ]
}
```

#### 6. Create Food Entry
**POST** `/api/foods/`

**Request Body:**
```json
{
  "name": "Grilled Chicken Breast",
  "calories": 231,
  "nutrients": {
    "protein": 43.5,
    "carbs": 0,
    "fats": 5.0,
    "fiber": 0
  }
}
```

#### 7. Get Food Entry
**GET** `/api/foods/{id}/`

#### 8. Update Food Entry
**PUT/PATCH** `/api/foods/{id}/`

#### 9. Delete Food Entry
**DELETE** `/api/foods/{id}/`

---

### Diet Plan Endpoints

#### 10. List Diet Plans
**GET** `/api/diet-plans/`

#### 11. Create Diet Plan
**POST** `/api/diet-plans/`

**Request Body:**
```json
{
  "plan": {
    "daily_calorie_target": 2000,
    "macros": {
      "protein_grams": 150,
      "carbs_grams": 250,
      "fats_grams": 67
    },
    "weekly_plan": {
      "monday": [
        {
          "meal": "breakfast",
          "name": "Oatmeal with fruits",
          "calories": 350,
          "nutrients": {...}
        }
      ]
    }
  },
  "is_active": true
}
```

#### 12. Get/Update/Delete Diet Plan
**GET/PUT/PATCH/DELETE** `/api/diet-plans/{id}/`

---

### Workout Endpoints

#### 13. List Workouts
**GET** `/api/workouts/`

#### 14. Create Workout
**POST** `/api/workouts/`

**Request Body:**
```json
{
  "workout": {
    "weekly_schedule": {
      "monday": [
        {
          "exercise": "Squats",
          "sets": 3,
          "reps": "10-12",
          "duration": "30 min"
        }
      ]
    },
    "rest_days": ["sunday"],
    "difficulty": "intermediate"
  },
  "is_active": true
}
```

---

### Analytics Endpoints

#### 15. Get Analytics
**GET** `/api/analytics/?days=30`

**Response (200 OK):**
```json
{
  "period_days": 30,
  "start_date": "2023-12-16T10:30:00Z",
  "end_date": "2024-01-15T10:30:00Z",
  "total_calories": 45000,
  "average_calories_per_day": 1500.0,
  "days_logged": 30,
  "total_nutrients": {
    "protein": 1500,
    "carbs": 2000,
    "fats": 800,
    "fiber": 600
  },
  "daily_calories": {
    "2024-01-15": 1500,
    "2024-01-14": 1650,
    ...
  },
  "total_food_entries": 90
}
```

---

### AI Integration Endpoints (FastAPI via Django)

#### 16. Chatbot Query
**POST** `/api/chatbot/query/`

**Request Body:**
```json
{
  "query": "What are some healthy breakfast options?"
}
```

**Response (200 OK):**
```json
{
  "response": "Here are some healthy breakfast options...",
  "query": "What are some healthy breakfast options?"
}
```

#### 17. Generate Diet Plan
**POST** `/api/diet/generate/`

**Response (201 Created):**
```json
{
  "id": 1,
  "user": "user@example.com",
  "plan": {
    "daily_calorie_target": 2000,
    "weekly_plan": {...},
    "workout_plan": {...}
  },
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

#### 18. Analyze Food
**POST** `/api/food/analyze/`

**Request Body:**
```json
{
  "name": "Grilled Chicken Breast"
}
```

**Response (200 OK):**
```json
{
  "name": "Grilled Chicken Breast",
  "calories": 231.0,
  "nutrients": {
    "protein": 43.5,
    "carbs": 0,
    "fats": 5.0,
    "fiber": 0
  },
  "serving_size": "100g"
}
```

#### 19. Nearby Restaurants
**GET** `/api/restaurant/nearby/?latitude=40.7128&longitude=-74.0060&radius=5000`

**Response (200 OK):**
```json
{
  "restaurants": [
    {
      "name": "Green Leaf Cafe",
      "location": {
        "latitude": 40.7128,
        "longitude": -74.0060
      },
      "address": "123 Healthy Street",
      "rating": 4.5,
      "healthy_options": [
        "Organic Kale Salad",
        "Grilled Salmon Bowl"
      ]
    }
  ]
}
```

---

## FastAPI Direct Endpoints

### Chatbot

**POST** `http://localhost:8001/chatbot/query`
- Same as Django endpoint `/api/chatbot/query/`

### Diet Generation

**POST** `http://localhost:8001/diet/generate`
- Same as Django endpoint `/api/diet/generate/`

### Food Analysis

**POST** `http://localhost:8001/food/analyze`
- Same as Django endpoint `/api/food/analyze/`

### Restaurant Search

**GET** `http://localhost:8001/restaurant/nearby`
- Same as Django endpoint `/api/restaurant/nearby/`

---

## Error Responses

All endpoints return standard HTTP status codes:

- **200 OK**: Successful GET/PUT/PATCH request
- **201 Created**: Successful POST request
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

**Error Response Format:**
```json
{
  "error": "Error message description"
}
```
