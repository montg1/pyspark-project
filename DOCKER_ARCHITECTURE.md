# 🐳 Docker Compose Architecture - Visual Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HOST MACHINE (macOS)                         │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                  Docker Desktop                              │ │
│  │                                                               │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │        Docker Engine & Daemon                          │ │ │
│  │  │                                                         │ │ │
│  │  │  ┌──────────────────────────────────────────────────┐  │ │ │
│  │  │  │       Bridge Network: app-network               │  │ │ │
│  │  │  │                                                  │  │ │ │
│  │  │  │  ┌──────────────────┐    ┌──────────────────┐  │  │ │ │
│  │  │  │  │   Frontend       │    │   Backend        │  │  │ │ │
│  │  │  │  │   (Nginx)        │    │   (FastAPI)      │  │  │ │ │
│  │  │  │  │   Port 80        │───→│   Port 8000      │  │  │ │ │
│  │  │  │  │                  │ /  │                  │  │  │ │ │
│  │  │  │  │ • Vue 3 SPA      │ api│ • 7 Endpoints    │  │  │ │ │
│  │  │  │  │ • Chart.js       │ *  │ • DataReader     │  │  │ │ │
│  │  │  │  │ • TailwindCSS    │ \  │ • CORS           │  │  │ │ │
│  │  │  │  │ • Axios client   │    │ • Health check   │  │  │ │ │
│  │  │  │  └──────────────────┘    └─────────┬────────┘  │  │ │ │
│  │  │  │                                    │           │  │ │ │
│  │  │  │                          ┌─────────↓────────┐  │  │ │ │
│  │  │  │                          │ Shared Volume    │  │  │ │ │
│  │  │  │                          │ /app/output/     │  │  │ │ │
│  │  │  │                          │ (Parquet data)   │  │  │ │ │
│  │  │  │                          └──────────────────┘  │  │ │ │
│  │  │  │                                                  │  │ │ │
│  │  │  │  ┌──────────────────────────────────────────┐  │  │ │ │
│  │  │  │  │        ETL Service (PySpark)            │  │  │ │ │
│  │  │  │  │ • Transforms raw data                   │  │  │ │ │
│  │  │  │  │ • Outputs to /app/output/               │  │  │ │ │
│  │  │  │  │ • Runs once, then exits                 │  │  │ │ │
│  │  │  │  └──────────────────────────────────────────┘  │  │ │ │
│  │  │  │                                                  │  │ │ │
│  │  │  └──────────────────────────────────────────────────┘  │ │ │
│  │  │                                                         │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  │                                                               │ │
│  │  Volume Mounts (Host ↔ Container):                          │ │
│  │  • ./frontend/src → /app/src (frontend code hot-reload)    │ │
│  │  • ./src → /app/src (backend code hot-reload)              │ │
│  │  • ./output → /app/output (shared ETL data)                │ │
│  │  • ./data → /app/data (input data, read-only)              │ │
│  │  • ./config → /app/config (configuration)                  │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  Port Mappings:                                                    │
│  • 80:80     → Frontend (Nginx)                                  │
│  • 8000:8000 → Backend (FastAPI)                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                    User Browser (Localhost)
                              ↓
            ┌───────────────────────────────────────┐
            │    Open http://localhost              │
            │    See Wine Reviews Dashboard         │
            │    Connected to Backend API           │
            └───────────────────────────────────────┘
```

## Service Interaction Flow

### Request Flow
```
1. User opens http://localhost
   ↓
2. Browser connects to Port 80
   ↓
3. Nginx receives request
   ├─ If path = /assets → Serve Vue.js assets
   ├─ If path = /api/* → Proxy to backend:8000
   └─ If other path → Serve index.html (SPA routing)
   ↓
4. Frontend (Vue 3) loads
   ├─ Mounts App.vue
   ├─ Initializes components
   └─ Makes API calls to /api/*
   ↓
5. Nginx proxies /api/* requests to backend:8000
   ↓
6. FastAPI backend receives request
   ├─ DataReader loads Parquet data
   ├─ Processes request
   └─ Returns JSON response
   ↓
7. Nginx forwards response to browser
   ↓
8. Vue.js receives data
   ├─ Updates component state
   ├─ Renders charts
   ├─ Renders tables
   └─ Displays results
   ↓
9. Dashboard shows wine data! 🍷
```

## Networking Model

```
┌─────────────────────────────────────────────────┐
│       Docker Host (app-network bridge)          │
├─────────────────────────────────────────────────┤
│                                                 │
│  Container Frontend              Container Backend
│  IP: 172.20.0.2                  IP: 172.20.0.3
│  Hostname: frontend              Hostname: backend
│  Port: 80 (internal)             Port: 8000 (internal)
│                                                 │
│  Exposed to Host:                Exposed to Host:
│  0.0.0.0:80→80                   0.0.0.0:8000→8000
│                                                 │
│  Can reach Backend:              Can reach Frontend:
│  http://backend:8000             http://frontend:80
│                                                 │
└─────────────────────────────────────────────────┘
       ↑                    ↑
       │ HTTP/80            │ HTTP/8000
       └────────────────────┘
             Host Machine
```

## Data Flow Architecture

```
┌─────────────────────┐
│   Raw Wine Data     │
│   (129,975 records) │
│   ./data/*.csv      │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────────┐
│   ETL Service (PySpark)         │
├─────────────────────────────────┤
│ • Extract raw data              │
│ • Transform/clean               │
│ • Aggregate statistics          │
│ • Load to Parquet format        │
└──────────┬──────────────────────┘
           │
           ↓
┌──────────────────────────────────┐
│ Transformed Data (Parquet)       │
│ (58,705 records)                 │
│ ./output/transformed_wine_reviews│
│ • countries.parquet              │
│ • wines.parquet                  │
│ • quality_dist.parquet           │
│ • price_dist.parquet             │
└────────────┬─────────────────────┘
             │
             ↓ (Volume Mount)
┌─────────────────────────────────┐
│  Backend Service (FastAPI)      │
├─────────────────────────────────┤
│ DataReader:                     │
│ • Loads Parquet files           │
│ • Provides query methods        │
│ • Serves 7 REST endpoints       │
└────────────┬────────────────────┘
             │
             ↓ (JSON Responses)
┌─────────────────────────────────┐
│  Frontend (Vue 3 Dashboard)     │
├─────────────────────────────────┤
│ Components:                     │
│ • StatsCard (4 metrics)         │
│ • QualityChart (doughnut)       │
│ • PriceChart (bar)              │
│ • TopVarietiesTable             │
│ • CountriesTable                │
└─────────────────────────────────┘
```

## Docker Compose Service Dependencies

```
docker-compose.yml
├── services:
│   ├── backend
│   │   ├── build: Dockerfile.backend
│   │   ├── ports: 8000:8000
│   │   ├── volumes:
│   │   │   ├── ./src → /app/src
│   │   │   └── ./output → /app/output
│   │   ├── environment:
│   │   │   ├── PYTHONPATH=/app/src
│   │   │   └── PYTHONUNBUFFERED=1
│   │   ├── networks: [app-network]
│   │   ├── healthcheck: curl /health
│   │   └── restart: unless-stopped
│   │
│   ├── frontend
│   │   ├── build: frontend/Dockerfile
│   │   ├── ports: 80:80
│   │   ├── depends_on: [backend]
│   │   ├── volumes: (via Dockerfile)
│   │   ├── networks: [app-network]
│   │   ├── healthcheck: wget /
│   │   └── restart: unless-stopped
│   │
│   ├── etl
│   │   ├── build: Dockerfile
│   │   ├── volumes:
│   │   │   ├── ./data → /app/data (ro)
│   │   │   └── ./output → /app/output
│   │   ├── environment: [PYTHONPATH, PYTHONUNBUFFERED]
│   │   ├── networks: [app-network]
│   │   ├── depends_on: [backend]
│   │   └── command: python -c "run_etl_pipeline()"
│   │
│   ├── etl-dev (profile: dev)
│   │   └── ... development environment
│   │
│   └── test (profile: test)
│       └── ... test runner
│
├── networks:
│   └── app-network: bridge
│
└── volumes:
    └── output: local driver
```

## Container Lifecycle

```
┌─────────────────────────────────────┐
│   docker-compose up -d              │
│   (Start all services)              │
└────────────┬────────────────────────┘
             │
             ├──→ Build backend image (if needed)
             ├──→ Build frontend image (if needed)
             └──→ Build ETL image (if needed)
                      │
                      ↓
             ┌────────────────────┐
             │  Create containers │
             ├────────────────────┤
             │ • backend          │
             │ • frontend         │
             │ • etl              │
             └────────┬───────────┘
                      │
                      ↓
             ┌────────────────────┐
             │  Start containers  │
             ├────────────────────┤
             │ 1. etl starts      │
             │ 2. backend starts  │
             │ 3. frontend starts │
             └────────┬───────────┘
                      │
                      ↓
             ┌────────────────────┐
             │  Health checks     │
             ├────────────────────┤
             │ ✓ backend healthy  │
             │ ✓ frontend healthy │
             │ ✓ etl exited ok    │
             └────────┬───────────┘
                      │
                      ↓
    ┌─────────────────────────────────┐
    │  Ready to accept requests!      │
    │  http://localhost ready         │
    │  http://localhost:8000 ready    │
    └─────────────────────────────────┘
```

## File Structure with Docker

```
pyspark/
├── docker-compose.yml           ← Main orchestration
├── Dockerfile                   ← ETL image (PySpark)
├── Dockerfile.backend           ← Backend image (FastAPI)
├── .dockerignore                ← Build optimization
│
├── frontend/
│   ├── Dockerfile              ← Frontend image (Nginx)
│   ├── nginx.conf              ← Nginx configuration
│   ├── .dockerignore           ← Build optimization
│   ├── src/
│   │   ├── App.vue             ← Main dashboard
│   │   ├── api/
│   │   │   └── client.js       ← Axios client
│   │   └── components/         ← Vue components
│   └── package.json            ← Node dependencies
│
├── src/
│   ├── api/
│   │   ├── main.py             ← FastAPI app
│   │   └── data_reader.py      ← Data utility
│   ├── etl/
│   │   └── etl.py              ← PySpark pipeline
│   └── tests/                  ← Test suite
│
├── data/                        ← Raw input (host volume)
├── output/                      ← Transformed data (host volume)
├── config/                      ← Configuration (host volume)
│
├── docker-start.sh             ← Startup script
├── DOCKER_QUICKSTART.md        ← Quick start
├── DOCKER_GUIDE.md             ← Detailed guide
├── DOCKER_SETUP_SUMMARY.md     ← Setup summary
├── DOCKER_VERIFICATION.md      ← Verification checklist
└── Makefile                    ← Command shortcuts
```

## Deployment Scenarios

### Local Development
```
Host Machine → Port 80 → Nginx → /api/* → FastAPI (Port 8000)
                ↓
         Vue.js Development
         Auto Hot Reload
         Live Code Updates
```

### Production Deployment
```
Load Balancer → Port 80 → Nginx → /api/* → FastAPI
                 (HTTPS)          (Health checks)
                ↓
    Multiple replicas possible
    Kubernetes orchestration
    Container registry (Docker Hub)
```

### CI/CD Pipeline
```
Git Push
  ↓
GitHub Actions
  ↓
├─ Run tests: docker-compose --profile test up test
├─ Build images: docker-compose build
├─ Push to registry: docker push
  ↓
Deploy
  ↓
docker-compose -f docker-compose.prod.yml up
```

## Key Connections Summary

| From | To | Protocol | Port | Type |
|------|-----|----------|------|------|
| Browser | Frontend | HTTP | 80 | External |
| Browser | Backend Docs | HTTP | 8000 | External |
| Frontend (Nginx) | Backend (FastAPI) | HTTP | 8000 | Internal Network |
| Frontend | Shared Volume | filesystem | - | Mount |
| Backend | Shared Volume | filesystem | - | Mount |
| ETL | Shared Volume | filesystem | - | Mount |

This is your complete Docker Compose architecture! 🐳🍷
