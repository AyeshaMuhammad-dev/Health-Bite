# Quick Start Guide

## Prerequisites Checklist

- [ ] Docker and Docker Compose installed
- [ ] OpenAI API key (required for AI features)
- [ ] Optional: Nutritionix API credentials (for food analysis)
- [ ] Optional: Google Maps API key (for restaurant filtering)

## Step-by-Step Setup

### 1. Clone and Navigate
```bash
cd health_bite_backend
```

### 2. Configure Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env file and add your API keys
# At minimum, add:
# OPENAI_API_KEY=your-key-here
```

### 3. Start Services
```bash
docker-compose up -d
```

Wait for services to start (check logs):
```bash
docker-compose logs -f
```

### 4. Run Database Migrations
```bash
docker-compose exec django python manage.py migrate
```

### 5. Create Admin User (Optional)
```bash
docker-compose exec django python manage.py createsuperuser
```

### 6. Verify Services

- Django API: http://localhost:8000/api/
- FastAPI: http://localhost:8001/
- FastAPI Docs: http://localhost:8001/docs
- Django Admin: http://localhost:8000/admin/

## Test the API

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

Save the `access` token from the response.

### 2. Log Food Entry
```bash
curl -X POST http://localhost:8000/api/foods/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Apple",
    "calories": 52,
    "nutrients": {"protein": 0.3, "carbs": 14}
  }'
```

### 3. Test Chatbot
```bash
curl -X POST http://localhost:8000/api/chatbot/query/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "query": "What are healthy breakfast options?"
  }'
```

### 4. Generate Diet Plan
```bash
curl -X POST http://localhost:8000/api/diet/generate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Common Commands

### View Logs
```bash
docker-compose logs -f django
docker-compose logs -f fastapi
docker-compose logs -f mysql
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Access Django Shell
```bash
docker-compose exec django python manage.py shell
```

### Access MySQL Database
```bash
docker-compose exec mysql mysql -u root -p health_bite_db
# Password: rootpassword
```

## Troubleshooting

### Services Won't Start
- Check if ports 8000, 8001, 3306 are available
- Check Docker logs: `docker-compose logs`

### Database Connection Errors
- Wait for MySQL to fully start (check health status)
- Verify `.env` file has correct database credentials

### FastAPI Can't Connect to OpenAI
- Verify `OPENAI_API_KEY` is set in `.env`
- Check FastAPI logs: `docker-compose logs fastapi`

### Django Migrations Fail
- Ensure MySQL is running: `docker-compose ps`
- Try: `docker-compose exec django python manage.py migrate --run-syncdb`

## Next Steps

- Read [API Documentation](docs/api_endpoints.md)
- Check [Architecture Overview](docs/architecture.md)
- Review [README.md](README.md) for full details
