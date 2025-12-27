# Running Health-Bite Without Docker

## ✅ Dependencies Installed
- ✅ Django and DRF dependencies (using PyMySQL for Windows compatibility)
- ✅ FastAPI dependencies
- All Python packages are installed!

## ⚠️ Required: MySQL Database

You need a MySQL database running. Options:

### Option 1: Install MySQL Locally

1. **Download MySQL**:
   - Visit: https://dev.mysql.com/downloads/installer/
   - Download MySQL Installer for Windows

2. **Install MySQL**:
   - Run the installer
   - Set root password (remember it!)
   - Create database: `health_bite_db`

3. **Update .env file**:
   ```env
   MYSQL_HOST=localhost
   MYSQL_DATABASE=health_bite_db
   MYSQL_USER=root
   MYSQL_PASSWORD=your-mysql-root-password
   MYSQL_PORT=3306
   ```

### Option 2: Use Docker for MySQL Only

If you can install Docker Desktop, you can run just MySQL in Docker:

```powershell
docker run --name health_bite_mysql -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=health_bite_db -p 3306:3306 -d mysql:8.0
```

Update `.env`:
```env
MYSQL_HOST=localhost
MYSQL_DATABASE=health_bite_db
MYSQL_USER=root
MYSQL_PASSWORD=rootpassword
MYSQL_PORT=3306
```

## 📝 Running the Project

### 1. Update Environment Variables

Edit `.env` file in `health_bite_backend/`:
```env
# Required
DJANGO_SECRET_KEY=django-insecure-change-me-in-production
MYSQL_HOST=localhost  # or mysql if using Docker
MYSQL_DATABASE=health_bite_db
MYSQL_USER=root
MYSQL_PASSWORD=your-password-here
OPENAI_API_KEY=your-openai-api-key-here  # Required for AI features

# Optional
NUTRITIONIX_APP_ID=your-key
NUTRITIONIX_API_KEY=your-key
GOOGLE_MAPS_API_KEY=your-key
```

### 2. Run Django Migrations

```powershell
cd D:\Health-Bite\health_bite_backend\django_core
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)

```powershell
python manage.py createsuperuser
```

### 4. Start Django Server

```powershell
python manage.py runserver
```

Django will run on: **http://localhost:8000**

### 5. Start FastAPI Server (New Terminal)

```powershell
cd D:\Health-Bite\health_bite_backend\fastapi_ai
uvicorn main:app --reload --port 8001
```

FastAPI will run on: **http://localhost:8001**

## 🎯 Access Points

- **Django API**: http://localhost:8000/api/
- **FastAPI**: http://localhost:8001/
- **FastAPI Docs**: http://localhost:8001/docs
- **Django Admin**: http://localhost:8000/admin/

## 🔧 Troubleshooting

### "Can't connect to MySQL server"
- Make sure MySQL is running
- Check MySQL credentials in `.env`
- Verify MySQL is listening on port 3306

### PyMySQL Import Error
- Make sure PyMySQL is installed: `pip install PyMySQL`
- Check that settings.py has the PyMySQL configuration

### Port Already in Use
- Change ports in run commands:
  - Django: `python manage.py runserver 8000`
  - FastAPI: `uvicorn main:app --port 8001`

## 📚 Next Steps

1. Make sure MySQL is running
2. Update `.env` with your MySQL credentials
3. Run migrations
4. Start both servers
5. Test the API endpoints!
