from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os

# Load environment variables
load_dotenv()

from app.routes import auth, persona, persona_builder, strategy, script, feedback, persona_refine, preferences
from app.routes.enhanced_persona import router as enhanced_persona_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Or for more detailed logs during development
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)


app = FastAPI(title="Creator AI API", version="2.0.0")

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(persona.router)
app.include_router(persona_builder.router)
app.include_router(enhanced_persona_router)  # New enhanced persona routes
app.include_router(strategy.router)
app.include_router(script.router)
app.include_router(feedback.router)
app.include_router(persona_refine.router)
app.include_router(preferences.router)

@app.get("/")
def read_root():
    return {"message": "Creator AI API v2.0 - Enhanced Multi-Modal Persona System"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}