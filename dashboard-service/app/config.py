import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = os.getenv("POSTGRES_USER", "sentinelx")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "sentinelx_pass")
    postgres_db: str = os.getenv("POSTGRES_DB", "sentinelx_db")
    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    kafka_output_topic: str = os.getenv("KAFKA_OUTPUT_TOPIC", "agent-recommendations")
    kafka_group_id: str = os.getenv("KAFKA_GROUP_ID", "dashboard-service-group")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()