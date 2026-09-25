
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SIGNSYNC API",
    description="AI-Powered Indian Sign Language Translator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "application": "SIGNSYNC",
        "description": "Indian Sign Language Translator",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/api/health")
async def health_check():
    return {
        "application": "SIGNSYNC",
        "status": "healthy",
        "version": "1.0.0",
    }
