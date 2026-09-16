# ai-orchestrator/app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Kafka -- consumes what the Incident Service publishes
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_input_topic: str = "incidents"
    kafka_output_topic: str = "agent-recommendations"
    kafka_consumer_group: str = "ai-orchestrator"

    # LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    # RAG service (Step 13)
    rag_service_url: str = "http://rag-service:8000"

    # Digital Twin (Step 14)
    digital_twin_url: str = "http://digital-twin:8000"
    digital_twin_entrypoint: str = "Internet"

    class Config:
        env_file = ".env"


settings = Settings()
