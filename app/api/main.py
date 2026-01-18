import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

# Initialize FastAPI with metadata
app = FastAPI(
    title="Avatar AI Backend",
    description="Production-ready API for LiveKit Token generation",
    version="1.0.0"
)

# 1. Flexible CORS Configuration
# Pulls allowed origins from environment variables for production security
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:8000")
origins = [origin.strip() for origin in raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restrict to necessary methods for security
    allow_headers=["*"],
)

# 2. Health Check Endpoint
@app.get("/", tags=["System"])
async def root():
    """
    Used by cloud load balancers to verify the service is live.
    """
    return {
        "status": "online",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0"
    }

# Include the routes for token generation
app.include_router(router)

# 3. Production-Ready Entrypoint
if __name__ == "__main__":
    # Pull the port from the environment variable provided by the cloud platform
    # Defaults to 8000 for local development
    port = int(os.getenv("PORT", 8000))
    
    # Use 0.0.0.0 to bind to all interfaces, which is required for cloud hosting
    # Toggle reload based on environment to ensure stability in production
    is_dev = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"🚀 Starting Server on port {port} (Dev Mode: {is_dev})")
    uvicorn.run(
        "app.api.main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=is_dev,
        workers=int(os.getenv("WEB_CONCURRENCY", 1))
    )