"""
Configuration for FastAPI application.
"""
import os

# Database
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'health_bite_db')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'rootpassword')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Nutrition APIs
NUTRITIONIX_APP_ID = os.getenv('NUTRITIONIX_APP_ID', '')
NUTRITIONIX_API_KEY = os.getenv('NUTRITIONIX_API_KEY', '')
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID', '')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY', '')

# Google Maps
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
