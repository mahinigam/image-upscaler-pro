#!/bin/bash

# Kill any running instances
pkill -f uvicorn
pkill -f vite

echo "🚀 Starting Image Upscaler Pro..."

# Start Backend
echo "Starting Backend on port 8000..."
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start Frontend
echo "Starting Frontend on port 3000..."
cd frontend
npm run dev -- --port 3000 &
FRONTEND_PID=$!

echo "✅ App is running!"
echo "➡️  Frontend: http://localhost:3000"
echo "➡️  Backend:  http://localhost:8000"

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
