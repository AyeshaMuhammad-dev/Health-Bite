"""
FastAPI main application for Health-Bite AI microservices.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import mysql.connector
from mysql.connector import Error

from .routes import chatbot, diet, food, restaurant

# Database connection pool
db_pool = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    global db_pool
    try:
        db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="health_bite_pool",
            pool_size=5,
            pool_reset_session=True,
            host=os.getenv('MYSQL_HOST', 'mysql'),
            database=os.getenv('MYSQL_DATABASE', 'health_bite_db'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'rootpassword'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
        )
        print("Database connection pool created successfully")
    except Error as e:
        print(f"Error creating database pool: {e}")
    
    yield
    
    # Shutdown
    if db_pool:
        db_pool._remove_connections()
        print("Database connection pool closed")


app = FastAPI(
    title="Health-Bite AI Services",
    description="Microservice layer for AI-powered features",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(diet.router, prefix="/diet", tags=["Diet"])
app.include_router(food.router, prefix="/food", tags=["Food"])
app.include_router(restaurant.router, prefix="/restaurant", tags=["Restaurant"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Health-Bite AI Services API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Export app for uvicorn
__all__ = ["app"]
