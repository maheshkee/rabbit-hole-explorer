from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# These will be created in next steps
# from app.api.v1.api import api_router
# from app.core.config import settings

def get_application() -> FastAPI:
    _app = FastAPI(
        title="AI Internet Rabbit Hole Explorer",
        description="AI-driven concept exploration engine",
        version="0.1.0",
    )

    # Set all CORS enabled origins
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, restrict this.
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API Routers (placeholder until we define the api_router)
    # _app.include_router(api_router, prefix="/api/v1")

    return _app

app = get_application()

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
