#!/bin/bash

# Docker Compose startup script for Wine Reviews Platform
# Usage: ./docker-start.sh

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🍷 Wine Reviews Platform - Docker Compose Startup"
echo "=================================================="
echo ""

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon is not running. Please start Docker."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Navigate to project directory
cd "$PROJECT_DIR"
echo "📁 Working directory: $PROJECT_DIR"
echo ""

# Check if docker-compose file exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    exit 1
fi

echo "🔨 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🏥 Checking service health..."

# Check backend
if docker-compose exec -T backend curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend (FastAPI) is running on http://localhost:8000"
else
    echo "⏳ Backend is starting, check logs with: docker-compose logs -f backend"
fi

# Check frontend
if docker-compose exec -T frontend wget -q --tries=1 -O - http://localhost/ > /dev/null 2>&1; then
    echo "✅ Frontend (Nginx) is running on http://localhost"
else
    echo "⏳ Frontend is building/starting, check logs with: docker-compose logs -f frontend"
fi

echo ""
echo "=================================================="
echo "🎉 Services are starting up!"
echo ""
echo "📊 Dashboard: http://localhost"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🔧 API Redoc: http://localhost:8000/redoc"
echo ""
echo "📋 Useful commands:"
echo "  docker-compose logs -f          # View all logs"
echo "  docker-compose logs -f backend  # View backend logs"
echo "  docker-compose logs -f frontend # View frontend logs"
echo "  docker-compose ps               # Show all services"
echo "  docker-compose down             # Stop all services"
echo ""
echo "Or use: make docker-logs, make docker-ps, make docker-down"
echo "=================================================="
