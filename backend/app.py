# backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from api.websocket import websocket_endpoint  # If you have WebSocket endpoints

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix='/api')

# Include WebSocket routes if any
app.add_api_websocket_route("/ws", websocket_endpoint)

# **Add this root route**
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Stock Trading System API"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)