import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze

app = FastAPI(title="Phishing URL Analyzer", version="1.0.0")

# CORS Setup
origins = [
    "http://localhost:5173", # Vite default
    "http://127.0.0.1:5173",
    os.getenv("FRONTEND_URL"),
]
# Filter out None values
origins = [o for o in origins if o]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])

@app.get("/")
def read_root():
    return {"status": "Phishing Analyzer Operational", "version": "1.0.0"}
