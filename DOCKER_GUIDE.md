# Docker Compose Setup Guide

This Docker Compose configuration orchestrates the complete wine reviews data exploration platform with ETL pipeline, FastAPI backend, and Vue 3 frontend.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│   Frontend (Vue 3 + Nginx on port 80)   │
│   http://localhost                      │
└──────────────────┬──────────────────────┘
                   │
                   ↓ /api proxy
┌─────────────────────────────────────────┐
│   Backend (FastAPI on port 8000)        │
│   http://localhost:8000                 │
└──────────────────┬──────────────────────┘
                   │
                   ↓ reads data
┌─────────────────────────────────────────┐
│   Output Data (Parquet files)           │
│   /output/transformed_wine_reviews      │
└─────────────────────────────────────────┘
```

## 📦 Services

### 1. **ETL Service**
- **Image**: Python 3.9 + Java 11 + PySpark
- **Purpose**: Runs data transformation pipeline
- **Volumes**: 
  - `data/` (read-only) - Raw data input
  - `output/` - Transformed data (Parquet)
- **Command**: Executes PySpark ETL pipeline

### 2. **Backend Service**
- **Image**: Python 3.9 + FastAPI + PySpark
- **Port**: 8000
- **Purpose**: REST API server for wine data queries
- **Endpoints**:
  - `GET /health` - Health check
  - `GET /stats/countries` - Country statistics
  - `GET /stats/quality-distribution` - Quality breakdown
  - `GET /stats/price-distribution` - Price breakdown
  - `GET /stats/top-varieties` - Top wine varieties
  - `GET /stats/total-count` - Total wine count
  - `GET /wines` - Paginated wine data
- **Features**: Auto-reload in Docker, health checks

### 3. **Frontend Service**
- **Image**: Node 20 (build) + Nginx (serve)
- **Port**: 80
- **Purpose**: Vue 3 dashboard
- **Features**: 
  - API proxy to backend (/api/ → backend:8000/)
  - Static asset serving
  - SPA routing with index.html fallback

### 4. **ETL Dev Service** (optional)
- **Profile**: `dev`
- **Purpose**: Manual ETL testing/debugging
- **Usage**: `docker-compose --profile dev run etl-dev bash`

### 5. **Test Service** (optional)
- **Profile**: `test`
- **Purpose**: Run pytest suite
- **Usage**: `docker-compose --profile test up test`

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- ~2GB disk space for images and data

### Start All Services

```bash
# Navigate to project directory
cd /Users/maverix/Desktop/mon/pyspark

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps
```

### Access the Application

- **Frontend Dashboard**: http://localhost (port 80)
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Redoc**: http://localhost:8000/redoc

## 📋 Common Commands

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f etl

# Last 100 lines
docker-compose logs --tail=100
```

### Run Services Individually
```bash
# Start only backend
docker-compose up backend

# Start only frontend
docker-compose up frontend

# Start backend and frontend (without ETL)
docker-compose up backend frontend
```

### Execute Commands in Running Container
```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# Run Python in backend
docker-compose exec backend python -c "import sys; print(sys.version)"
```

### Rebuild Services
```bash
# Rebuild all
docker-compose build --no-cache

# Rebuild specific service
docker-compose build --no-cache backend
docker-compose build --no-cache frontend
```

### Development Workflow
```bash
# Start services in the background
docker-compose up -d

# Make code changes, backend auto-reloads (--reload flag)
# Frontend needs rebuild:
docker-compose restart frontend

# Check specific service
docker-compose exec backend curl http://localhost:8000/health
```

### Optional Services (with --profile)
```bash
# Run tests
docker-compose --profile test up test

# Run ETL dev environment
docker-compose --profile dev up etl-dev
docker-compose --profile dev exec etl-dev bash
```

### Cleanup
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Remove all containers, networks, and volumes
docker-compose down --remove-orphans -v

# Prune unused Docker resources
docker system prune -a
```

## 🔧 Configuration

### Environment Variables
Edit `docker-compose.yml` to modify:
- `PYTHONPATH` - Python module search path
- `PYTHONUNBUFFERED` - Real-time log output

### Ports
- Frontend: `80` (HTTP) - Change in docker-compose.yml `ports: - "80:80"`
- Backend: `8000` - Change in docker-compose.yml `ports: - "8000:8000"`

### Volumes
Persistent directories:
- `./data/` - Input data (read-only)
- `./output/` - ETL output (shared between backend and ETL)
- `./src/` - Backend source (mounted for hot-reload)
- `./config/` - Configuration files

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
lsof -i :80

# Kill process
kill -9 <PID>
```

### Service Fails to Start
```bash
# Check logs
docker-compose logs backend

# Rebuild without cache
docker-compose build --no-cache backend
docker-compose up backend
```

### API Connection Failed
- Verify backend is running: `docker-compose ps`
- Check logs: `docker-compose logs backend`
- Test health endpoint: `curl http://localhost:8000/health`

### Frontend Shows Blank Page
- Check browser console for errors
- Verify backend is accessible: `curl http://localhost:8000/health`
- Check frontend logs: `docker-compose logs frontend`
- Rebuild frontend: `docker-compose build --no-cache frontend && docker-compose up frontend`

### ETL Data Not Generated
```bash
# Check if ETL service completed
docker-compose logs etl

# Check output directory
docker-compose exec backend ls -la /app/output/

# Run ETL manually
docker-compose exec backend python -c "from src.etl.etl import run_etl_pipeline; run_etl_pipeline()"
```

## 📊 Data Flow

```
Raw Data (./data/)
        ↓
   ETL Service
   (PySpark)
        ↓
Output Data (./output/transformed_wine_reviews/)
        ↓
Backend API
(DataReader loads Parquet)
        ↓
Frontend Dashboard
(Vue 3 + Chart.js)
```

## 🔐 Security Notes (Production)

- Change CORS `allow_origins=["*"]` in backend
- Use environment variables for sensitive data
- Add authentication layer
- Enable HTTPS
- Use proper secrets management

## 📈 Performance Tips

1. **Volume Performance**: Use named volumes instead of bind mounts on Mac (better I/O)
2. **Build Caching**: Don't modify requirements.txt unless necessary
3. **Rebuild Strategy**: Use multi-stage builds for smaller images
4. **Network**: Services on same bridge network communicate efficiently

## 🎯 Next Steps

1. Start services: `docker-compose up -d`
2. Open http://localhost in browser
3. Monitor logs: `docker-compose logs -f`
4. Test API: `curl http://localhost:8000/health`
5. Verify frontend connects to backend
