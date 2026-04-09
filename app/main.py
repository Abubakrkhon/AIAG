"""Interview.ai - Voice AI Hiring Screener for SMBs"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.models import init_db
from app.voice_agent.agent import VoiceAgent
from app.twilio.webhook import router as twilio_router
from app.integrations.zapier import router as zapier_router
from app.payments.subscriptions import router as payments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title="Interview.ai",
    description="Voice AI hiring screener for micro-SMBs and local businesses",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(twilio_router, prefix="/twilio", tags=["Twilio"])
app.include_router(zapier_router, prefix="/webhook", tags=["Integrations"])
app.include_router(payments_router, prefix="/payments", tags=["Payments"])


@app.get("/")
async def root():
    return {
        "name": "Interview.ai",
        "version": "1.0.0",
        "status": "running",
        "description": "Voice AI hiring screener for SMBs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
