# Health-Bite Backend Architecture

## Overview

Health-Bite is a microservices-based backend system for a health and nutrition application. It consists of two main services:

1. **Django REST Framework Core** - Handles user management, data persistence, and business logic
2. **FastAPI AI Microservice** - Handles AI-powered features like chatbot, diet generation, and food analysis

Both services share a common MySQL database.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Frontend)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│  Django REST    │    │   FastAPI AI     │
│  Framework      │◄───┤   Microservice   │
│  (Port 8000)    │    │   (Port 8001)    │
└────────┬────────┘    └──────────────────┘
         │                       │
         │                       │
         └───────────┬───────────┘
                     │
                     │ MySQL Protocol
                     │
                     ▼
         ┌──────────────────────┐
         │   MySQL Database     │
         │  (Port 3306)         │
         │  health_bite_db      │
         └──────────────────────┘
```

---

## Service Breakdown

### 1. Django REST Framework Core (`django_core/`)

**Purpose**: Core backend service for user management, data persistence, and API orchestration.

**Components**:
- **Models** (`core_app/models.py`): Database models for User, Food, DietPlan, Workout, Restaurant
- **Serializers** (`core_app/serializers.py`): Data serialization/deserialization
- **Views** (`core_app/views.py`): API endpoints and request handling
- **Services** (`core_app/services.py`): Business logic (Analytics, FastAPI communication)
- **URLs** (`core_app/urls.py`): URL routing

**Key Features**:
- JWT-based authentication
- User registration and login
- Profile management
- Food logging
- Diet/workout plan storage
- Analytics generation
- Integration with FastAPI services

**Database Models**:
- `User`: Custom user model with health profile fields
- `Food`: Food log entries with calories and nutrients
- `DietPlan`: JSON-stored diet plans
- `Workout`: JSON-stored workout plans
- `Restaurant`: Restaurant information

---

### 2. FastAPI AI Microservice (`fastapi_ai/`)

**Purpose**: AI-powered features and external API integrations.

**Components**:
- **Routes** (`routes/`): API endpoint handlers
  - `chatbot.py`: Nutrition/fitness Q&A
  - `diet.py`: Diet plan generation
  - `food.py`: Food nutrition analysis
  - `restaurant.py`: Healthy restaurant filtering
- **Services** (`services/`): External API integrations
  - `openai_service.py`: OpenAI GPT-4.1 integration
  - `nutrition_service.py`: Nutritionix/Edamam APIs
  - `maps_service.py`: Google Maps API

**Key Features**:
- OpenAI GPT-4.1 for chatbot and diet/workout generation
- Nutritionix/Edamam for food analysis
- Google Maps for restaurant search
- Async/await for better performance

---

## Database Schema

### Users Table
```sql
users
├── id (PK)
├── email (UNIQUE)
├── password (hashed)
├── name
├── age
├── gender
├── height
├── weight
├── goals (JSON)
├── is_active
├── is_staff
└── date_joined
```

### Foods Table
```sql
foods
├── id (PK)
├── user_id (FK → users)
├── name
├── calories
├── nutrients (JSON)
└── logged_at
```

### Diet Plans Table
```sql
diet_plans
├── id (PK)
├── user_id (FK → users)
├── plan (JSON)
├── created_at
├── updated_at
└── is_active
```

### Workouts Table
```sql
workouts
├── id (PK)
├── user_id (FK → users)
├── workout (JSON)
├── created_at
├── updated_at
└── is_active
```

### Restaurants Table
```sql
restaurants
├── id (PK)
├── name
├── location (JSON)
├── healthy_options (JSON)
└── created_at
```

---

## Technology Stack

### Backend Frameworks
- **Django 4.2.7**: Core REST API framework
- **Django REST Framework 3.14.0**: API building toolkit
- **FastAPI 0.104.1**: AI microservice framework

### Database
- **MySQL 8.0**: Primary database
- **mysqlclient**: Django MySQL adapter
- **mysql-connector-python**: FastAPI MySQL connector

### Authentication
- **djangorestframework-simplejwt 5.3.1**: JWT token authentication

### AI Services
- **OpenAI API**: GPT-4.1 for chatbot and plan generation
- **Nutritionix API**: Food nutrition data
- **Edamam API**: Alternative nutrition data source
- **Google Maps API**: Restaurant location and filtering

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Gunicorn**: Django WSGI server
- **Uvicorn**: FastAPI ASGI server

---

## Data Flow

### User Registration Flow
```
Client → Django POST /api/auth/register/
       → Django creates User
       → Django generates JWT tokens
       → Client receives tokens
```

### Food Logging Flow
```
Client → Django POST /api/foods/ (with JWT)
       → Django validates token
       → Django saves Food entry
       → Client receives confirmation
```

### Chatbot Query Flow
```
Client → Django POST /api/chatbot/query/ (with JWT)
       → Django validates token
       → Django calls FastAPI /chatbot/query
       → FastAPI calls OpenAI API
       → FastAPI returns response
       → Django returns to client
```

### Diet Plan Generation Flow
```
Client → Django POST /api/diet/generate/ (with JWT)
       → Django validates token
       → Django calls FastAPI /diet/generate
       → FastAPI calls OpenAI API
       → FastAPI returns plan JSON
       → Django saves DietPlan to database
       → Django returns to client
```

---

## Security Considerations

1. **JWT Authentication**: All protected endpoints require valid JWT tokens
2. **Password Hashing**: Django uses bcrypt for password storage
3. **CORS**: Configured for specific origins in production
4. **Environment Variables**: Sensitive data stored in `.env` files
5. **SQL Injection Prevention**: ORM usage prevents SQL injection
6. **API Rate Limiting**: Can be added via Django middleware

---

## Scalability

### Horizontal Scaling
- Django and FastAPI services can be scaled independently
- Load balancer can distribute requests across multiple instances
- Database connection pooling in both services

### Database Optimization
- Indexes on frequently queried fields
- JSON fields for flexible data storage
- Foreign key relationships for data integrity

### Caching Strategy (Future)
- Redis for session storage
- Cache frequently accessed data
- Cache AI-generated plans

---

## Development Workflow

1. **Local Development**:
   ```bash
   docker-compose up
   ```

2. **Database Migrations**:
   ```bash
   docker-compose exec django python manage.py makemigrations
   docker-compose exec django python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

4. **Run Tests**:
   ```bash
   docker-compose exec django python manage.py test
   pytest tests/
   ```

---

## API Integration Points

### Django ↔ FastAPI Communication
- Django uses `requests` library to call FastAPI
- FastAPI URL configured via `FASTAPI_URL` environment variable
- Default: `http://fastapi:8001` (internal Docker network)

### External APIs
- **OpenAI**: Configured via `OPENAI_API_KEY`
- **Nutritionix**: Configured via `NUTRITIONIX_APP_ID` and `NUTRITIONIX_API_KEY`
- **Edamam**: Configured via `EDAMAM_APP_ID` and `EDAMAM_APP_KEY`
- **Google Maps**: Configured via `GOOGLE_MAPS_API_KEY`

---

## Future Enhancements

1. **Redis Caching**: Add Redis for caching frequently accessed data
2. **Celery Tasks**: Async task processing for AI operations
3. **WebSocket Support**: Real-time updates for analytics
4. **API Versioning**: Version API endpoints for backward compatibility
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Monitoring**: Add logging and monitoring (e.g., Sentry, Prometheus)
7. **Testing**: Expand test coverage with integration tests
8. **Documentation**: Auto-generate API docs with Swagger/OpenAPI
