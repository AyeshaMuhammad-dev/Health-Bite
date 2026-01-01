# Health-Bite Backend

A comprehensive backend system for a health and nutrition application, built with Django REST Framework and FastAPI microservices.

## Architecture

- **Django REST Framework**: Core backend for user management, food logging, diet/workout plans, and analytics
- **FastAPI**: AI microservice for chatbot, diet generation, food analysis, and restaurant filtering
- **MySQL**: Shared database for both services
- **Docker**: Containerized setup for easy deployment

## Features

### Core Features (Django)
- ✅ User registration and login with JWT authentication
- ✅ User profile management (age, gender, height, weight, goals)
- ✅ Food logging with calories and nutrients
- ✅ Diet and workout plan storage
- ✅ Analytics and progress tracking
- ✅ Restaurant information storage

### AI Features (FastAPI)
- ✅ Nutrition/fitness chatbot using OpenAI GPT-4.1
- ✅ Personalized diet plan generation
- ✅ Workout plan generation
- ✅ Food nutrition analysis (Nutritionix/Edamam)
- ✅ Healthy restaurant filtering (Google Maps)

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- API keys for:
  - OpenAI (required for chatbot and plan generation)
  - Nutritionix/Edamam (optional, for food analysis)
  - Google Maps (optional, for restaurant filtering)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd health_bite_backend
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   NUTRITIONIX_APP_ID=your-nutritionix-app-id (optional)
   NUTRITIONIX_API_KEY=your-nutritionix-api-key (optional)
   GOOGLE_MAPS_API_KEY=your-google-maps-api-key (optional)
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec django python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

### Access Services

- **Django API**: http://localhost:8000/api/
- **FastAPI AI Services**: http://localhost:8001/
- **FastAPI Docs**: http://localhost:8001/docs
- **Django Admin**: http://localhost:8000/admin/

## API Documentation

### Django REST Framework Endpoints

#### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/token/refresh/` - Refresh JWT token

#### Profile
- `GET/PUT/PATCH /api/profile/` - Get/update user profile

#### Food Logging
- `GET /api/foods/` - List food entries
- `POST /api/foods/` - Create food entry
- `GET/PUT/PATCH/DELETE /api/foods/{id}/` - Food entry operations

#### Diet Plans
- `GET /api/diet-plans/` - List diet plans
- `POST /api/diet-plans/` - Create diet plan
- `GET/PUT/PATCH/DELETE /api/diet-plans/{id}/` - Diet plan operations

#### Workouts
- `GET /api/workouts/` - List workouts
- `POST /api/workouts/` - Create workout
- `GET/PUT/PATCH/DELETE /api/workouts/{id}/` - Workout operations

#### Analytics
- `GET /api/analytics/?days=30` - Get user analytics

#### AI Integration
- `POST /api/chatbot/query/` - Chatbot query
- `POST /api/diet/generate/` - Generate diet plan
- `POST /api/food/analyze/` - Analyze food nutrition
- `GET /api/restaurant/nearby/?lat={lat}&lng={lng}` - Find nearby restaurants

### FastAPI Endpoints

- `POST /chatbot/query` - Chatbot query
- `POST /diet/generate` - Generate diet plan
- `POST /food/analyze` - Analyze food
- `GET /restaurant/nearby` - Find nearby restaurants
- `GET /docs` - Interactive API documentation (Swagger UI)

## Example API Calls

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepass123",
    "password2": "securepass123",
    "age": 30,
    "gender": "male",
    "height": 175,
    "weight": 80
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### Log Food (with JWT token)
```bash
curl -X POST http://localhost:8000/api/foods/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Grilled Chicken Breast",
    "calories": 231,
    "nutrients": {
      "protein": 43.5,
      "carbs": 0,
      "fats": 5
    }
  }'
```

### Chatbot Query
```bash
curl -X POST http://localhost:8000/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "query": "What are some healthy breakfast options?"
  }'
```

### Generate Diet Plan
```bash
curl -X POST http://localhost:8000/api/diet/generate/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

```
health_bite_backend/
├── django_core/                 # Django REST Framework service
│   ├── core_app/               # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── serializers.py     # API serializers
│   │   ├── views.py           # API views
│   │   ├── services.py        # Business logic
│   │   └── urls.py            # URL routing
│   ├── django_core/           # Django project settings
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── fastapi_ai/                 # FastAPI microservice
│   ├── routes/                # API routes
│   │   ├── chatbot.py
│   │   ├── diet.py
│   │   ├── food.py
│   │   └── restaurant.py
│   ├── services/              # External API services
│   │   ├── openai_service.py
│   │   ├── nutrition_service.py
│   │   └── maps_service.py
│   ├── main.py               # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── database/                  # Database scripts
│   ├── schema.sql            # Database schema reference
│   └── init.sql              # Initialization script
├── tests/                    # Test suite
│   ├── test_django_views.py
│   ├── test_fastapi_routes.py
│   └── conftest.py
├── docs/                     # Documentation
│   ├── api_endpoints.md      # API documentation
│   └── architecture.md       # Architecture documentation
├── docker-compose.yml        # Docker orchestration
└── README.md
```

## Development

### Running Tests

```bash
# Django tests
docker-compose exec django python manage.py test

# FastAPI tests
docker-compose exec fastapi pytest tests/test_fastapi_routes.py
```

### Database Migrations

```bash
# Create migrations
docker-compose exec django python manage.py makemigrations

# Apply migrations
docker-compose exec django python manage.py migrate
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f django
docker-compose logs -f fastapi
docker-compose logs -f mysql
```

### Stopping Services

```bash
docker-compose down

# Remove volumes (clears database)
docker-compose down -v
```

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `DJANGO_SECRET_KEY`: Django secret key (required)
- `DEBUG`: Enable debug mode (True/False)
- `MYSQL_HOST`: MySQL host (default: mysql)
- `MYSQL_DATABASE`: Database name (default: health_bite_db)
- `MYSQL_USER`: MySQL user
- `MYSQL_PASSWORD`: MySQL password
- `OPENAI_API_KEY`: OpenAI API key (required for AI features)
- `NUTRITIONIX_APP_ID`: Nutritionix app ID (optional)
- `NUTRITIONIX_API_KEY`: Nutritionix API key (optional)
- `GOOGLE_MAPS_API_KEY`: Google Maps API key (optional)

## Database Schema

See `database/schema.sql` for the complete database schema reference.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
