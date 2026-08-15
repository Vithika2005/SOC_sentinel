from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "threat-intel"

    # all-MiniLM-L6-v2: free, open-source, 384-dim, fast enough for CPU
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384

    class Config:
        env_file = ".env"


settings = Settings()
