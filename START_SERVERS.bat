@echo off
echo Starting Health-Bite Backend Services...
echo.

echo [1/2] Starting Django Server on port 8000...
start "Django Server" cmd /k "cd /d D:\Health-Bite\health_bite_backend\django_core && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo [2/2] Starting FastAPI Server on port 8001...
start "FastAPI Server" cmd /k "cd /d D:\Health-Bite\health_bite_backend\fastapi_ai && uvicorn main:app --reload --port 8001"

echo.
echo Services starting in separate windows...
echo.
echo Django API: http://localhost:8000/api/
echo FastAPI: http://localhost:8001/
echo FastAPI Docs: http://localhost:8001/docs
echo.
pause
