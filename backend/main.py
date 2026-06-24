from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import generate, history, health, analytics

app = FastAPI(title="Monologue Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(generate.router, tags=["Generate"])
app.include_router(history.router, tags=["History"])
app.include_router(analytics.router, tags=["Analytics"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
