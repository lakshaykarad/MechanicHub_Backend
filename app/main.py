import logging
from fastapi import FastAPI

from MechanicHub_Backend.app.routers import mechanics
from .database import Base, engine
from .seed import seed_data
from MechanicHub_Backend.app.routers import service_requests 

logging.basicConfig(level=logging.INFO)
 
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Instant Mechanic API",
    version="1.0.0"
)

# Include routers
app.include_router(mechanics.router)
app.include_router(service_requests.router)

@app.on_event("startup")
def on_startup():
    """Seed database with initial data if empty."""
    seed_data()