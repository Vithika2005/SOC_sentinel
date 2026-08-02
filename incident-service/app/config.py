from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Kafka
    kafka_bootstrap_servers: str = "sentinelx-kafka:29092"
    kafka_input_topic: str = "sentinelx-security-events"
    kafka_output_topic: str = "incidents"
    kafka_consumer_group: str = "incident-service"

    # PostgreSQL
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@local-postgres:5432/enterprise_db"
    )

    correlation_window_minutes: int = 15

    bloom_filter_capacity: int = 100000

    bloom_filter_error_rate: float = 0.001

    class Config:
        env_file = ".env"


settings = Settings()
settings = Settings()

print("=" * 60)
print(settings.kafka_bootstrap_servers)
print(settings.database_url)
print(settings.kafka_input_topic)
print("=" * 60)