# 🚀 Docker Compose Setup - Complete Guide

## Overview

Your Wine Reviews Platform is now ready to run with Docker Compose! This setup orchestrates:

- **ETL Pipeline** (PySpark) - Transforms raw wine data
- **Backend API** (FastAPI) - Serves data endpoints on port 8000
- **Frontend Dashboard** (Vue 3 + Nginx) - Interactive UI on port 80

## 📋 Prerequisites

- Docker Desktop installed ([https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop))
- Docker Compose v2.0+ (included with Docker Desktop)
- ~2GB available disk space

## 🎯 Quick Start (30 seconds)

### Option 1: Using the startup script
```bash
cd /Users/maverix/Desktop/mon/pyspark
./docker-start.sh
```

### Option 2: Using Docker Compose directly
```bash
cd /Users/maverix/Desktop/mon/pyspark

# Build images and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 3: Using Make commands
```bash
cd /Users/maverix/Desktop/mon/pyspark
make docker-up
make docker-logs
```

## ✅ Verify It's Working

Once started, check:

1. **Frontend Dashboard**: http://localhost
2. **Backend API Docs**: http://localhost:8000/docs
3. **Check Services**:
   ```bash
   docker-compose ps
   ```

Expected output:
```
NAME                      STATUS
wine-dashboard-frontend   Up (healthy)
wine-api-backend          Up (healthy)
pyspark-etl              Exited (completed)
```

## 📁 Project Structure

```
pyspark/
├── docker-compose.yml          # Main orchestration file
├── Dockerfile                  # Backend Dockerfile
├── Dockerfile.backend          # FastAPI backend service
├── frontend/
│   ├── Dockerfile             # Frontend build + Nginx serve
│   ├── nginx.conf             # Nginx configuration
│   ├── src/
│   │   ├── App.vue            # Main dashboard component
│   │   ├── api/client.js      # Axios API client
│   │   └── components/        # Vue components
│   └── package.json           # Frontend dependencies
├── src/
│   ├── api/main.py            # FastAPI app
│   ├── api/data_reader.py     # Data loading utility
│   ├── etl/etl.py             # PySpark ETL pipeline
│   └── tests/                 # Test suite
├── data/                       # Raw input data
├── output/                     # Transformed data (Parquet)
└── DOCKER_GUIDE.md            # Detailed Docker guide
```

## 🔧 Common Commands

### Service Management
```bash
# Start services
make docker-up
docker-compose up -d

# Stop services
make docker-down
docker-compose down

# View logs
make docker-logs
docker-compose logs -f

# Check status
make docker-ps
docker-compose ps

# Rebuild images (no cache)
make docker-rebuild
docker-compose build --no-cache
```

### Access Services
```bash
# Backend shell
make docker-backend
docker-compose exec backend bash

# Frontend shell  
make docker-frontend
docker-compose exec frontend sh

# Run command in backend
docker-compose exec backend python -c "print('Hello')"
```

### Troubleshooting
```bash
# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# View ETL logs
docker-compose logs etl

# Clean up everything
make docker-clean
docker-compose down -v --remove-orphans

# Test backend health
curl http://localhost:8000/health

# List all containers
docker-compose ps -a
```

## 🏗️ Architecture Diagram

```
Internet
    ↓
Port 80 (HTTP)
    ↓
Nginx Container (Frontend)
    ├── Serves Vue.js SPA
    │
    └── /api/* requests → Port 8000
            ↓
        Port 8000 (Internal network)
            ↓
        FastAPI Container (Backend)
            ├── Handles API requests
            │
            └── Reads Parquet data
                    ↓
                /app/output/ volume
                    ↓
                ETL-generated data
```

## 📊 Data Flow

1. **ETL Service** runs and generates transformed data in `/output/`
2. **Backend Service** starts and exposes 7 REST endpoints
3. **Frontend Service** builds Vue app and starts Nginx
4. **Frontend** calls `/api/*` endpoints which proxy to `backend:8000`
5. **Dashboard** displays live wine data with charts and tables

## 🔌 API Endpoints

Available at `http://localhost:8000`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Service health check |
| `/stats/countries` | GET | Country statistics |
| `/stats/quality-distribution` | GET | Quality breakdown |
| `/stats/price-distribution` | GET | Price breakdown |
| `/stats/top-varieties` | GET | Top 10-15 varieties |
| `/stats/total-count` | GET | Total wine count |
| `/wines` | GET | Paginated wine data |

Interactive documentation: http://localhost:8000/docs

## 🛑 Stopping Services

### Stop all services
```bash
docker-compose down
```

### Stop and remove data volumes
```bash
docker-compose down -v
```

### Stop one service
```bash
docker-compose stop backend
```

### Stop and remove specific container
```bash
docker-compose rm -f backend
```

## 🔍 View Logs in Real-time

```bash
# All services
docker-compose logs -f

# Specific service with last 50 lines
docker-compose logs --tail=50 -f backend

# Follow logs from multiple services
docker-compose logs -f backend frontend
```

## ⚙️ Environment Variables

Edit `docker-compose.yml` to modify:

```yaml
environment:
  - PYTHONPATH=/app/src
  - PYTHONUNBUFFERED=1
  # Add custom variables here
```

## 💾 Volumes

Persistent data locations:

- `./data/` → `/app/data` (input data, read-only)
- `./output/` → `/app/output` (ETL output, shared)
- `./src/` → `/app/src` (backend code, mounted for hot-reload)
- `./config/` → `/app/config` (configuration)

## 🔐 Production Notes

Before deploying to production:

1. Change CORS `allow_origins` in `src/api/main.py`
2. Set `--reload` to false in backend Dockerfile
3. Use environment variables for secrets
4. Add authentication layer
5. Enable HTTPS
6. Use proper database instead of Parquet
7. Implement proper logging and monitoring

## 🆘 Troubleshooting

### Port 80 already in use
```bash
# Change port in docker-compose.yml
# ports:
#   - "8080:80"  # Change from 80:80

docker-compose up -d
# Access at http://localhost:8080
```

### Port 8000 already in use
```bash
# Find what's using it
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Backend won't connect to frontend
1. Check both services are running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Test backend health: `curl http://localhost:8000/health`
4. Verify API endpoints: `curl http://localhost:8000/docs`

### Frontend shows blank page
1. Check console for errors (F12 → Console)
2. Check if backend is responding (see above)
3. Rebuild frontend: `docker-compose build --no-cache frontend`

### ETL data not found
```bash
# Check if ETL completed
docker-compose logs etl

# Check output directory
docker-compose exec backend ls -la /app/output/

# Manually run ETL
docker-compose exec backend python -c "from src.etl.etl import run_etl_pipeline; run_etl_pipeline()"
```

### Docker daemon not running
```bash
# On Mac, open Docker Desktop from Applications
# Or start from terminal:
open /Applications/Docker.app
```

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Vue 3 Documentation**: https://vuejs.org/
- **PySpark Documentation**: https://spark.apache.org/docs/latest/api/python/

## 📞 Support

For detailed troubleshooting and advanced configurations, see `DOCKER_GUIDE.md`
