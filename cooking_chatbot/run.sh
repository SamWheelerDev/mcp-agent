#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start the backend server in the background
echo "Starting backend server..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 57333 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Start the frontend
echo "Starting frontend..."
cd frontend
streamlit run app.py --server.port 53641 --server.address 0.0.0.0 --server.enableCORS true --server.enableXsrfProtection false

# Kill the backend when the script is terminated
kill $BACKEND_PID