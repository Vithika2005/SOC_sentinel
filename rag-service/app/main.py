from fastapi import FastAPI

from app.routers.rag_router import router as rag_router

app = FastAPI(title="SentinelX RAG Service", version="0.1.0")
app.include_router(rag_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
