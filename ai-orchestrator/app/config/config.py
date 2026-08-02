from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "SentinelX AI Orchestrator"
    HOST: str = "0.0.0.0"
    PORT: int = 8002

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CONSUMER_TOPIC: str = "incidents"
    KAFKA_PRODUCER_TOPIC: str = "agent-recommendations"

    class Config:
        env_file = ".env"


settings = Settings()