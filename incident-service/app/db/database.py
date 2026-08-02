"""
Singleton DB access (per your notes: #4 Singleton Pattern -> DB conn, Redis client, Qdrant client).
Everything else in the service depends on this module rather than creating its own engine.
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import settings

Base = declarative_base()


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_async_engine(
                settings.database_url,
                echo=False,
                pool_pre_ping=True,
            )
            cls._instance.session_factory = async_sessionmaker(
                cls._instance.engine, expire_on_commit=False
            )
        return cls._instance


db = Database()


async def get_db():
    """FastAPI dependency: yields a scoped session per request."""
    async with db.session_factory() as session:
        yield session


async def init_models():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
