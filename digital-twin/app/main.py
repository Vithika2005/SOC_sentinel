from fastapi import FastAPI

from app.routers.twin_router import router as twin_router

app = FastAPI(title="SentinelX Digital Twin", version="0.1.0")
app.include_router(twin_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
