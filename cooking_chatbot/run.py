import os
import subprocess
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_backend():
    """Run the FastAPI backend server"""
    backend_host = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port = os.getenv("BACKEND_PORT", "57333")
    
    print(f"Starting backend server on {backend_host}:{backend_port}...")
    
    # Start the backend server
    backend_process = subprocess.Popen(
        [
            sys.executable, 
            "-m", 
            "uvicorn", 
            "backend.api.main:app", 
            "--host", 
            backend_host, 
            "--port", 
            backend_port
        ],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    return backend_process

def run_frontend():
    """Run the Streamlit frontend"""
    frontend_port = os.getenv("FRONTEND_PORT", "53641")
    
    print(f"Starting frontend on port {frontend_port}...")
    
    # Start the frontend
    frontend_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "frontend/app.py",
            "--server.port",
            frontend_port,
            "--server.enableCORS=true",
            "--server.enableXsrfProtection=false",
            "--server.address=0.0.0.0"
        ],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    return frontend_process

if __name__ == "__main__":
    try:
        # Start the backend
        backend_process = run_backend()
        
        # Wait a moment for the backend to start
        time.sleep(2)
        
        # Start the frontend
        frontend_process = run_frontend()
        
        # Wait for processes to complete
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)