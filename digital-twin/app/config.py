from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "sentinelx123"

    # The root of your enterprise graph -- blast radius is computed as
    # "what becomes unreachable from here if this asset is isolated"
    default_entrypoint: str = "Internet"

    class Config:
        env_file = ".env"


settings = Settings()
