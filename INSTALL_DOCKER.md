# Installing Docker for Windows

This project is designed to run with Docker. Please follow these steps:

## Install Docker Desktop

1. **Download Docker Desktop for Windows**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Download and install Docker Desktop

2. **Start Docker Desktop**
   - After installation, start Docker Desktop
   - Wait for it to fully start (whale icon in system tray)

3. **Verify Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

4. **Run the Project**
   ```powershell
   cd D:\Health-Bite\health_bite_backend
   docker-compose up -d --build
   ```

## If Docker Compose Command Doesn't Work

Newer Docker versions use `docker compose` (without hyphen):
```powershell
docker compose up -d --build
```
