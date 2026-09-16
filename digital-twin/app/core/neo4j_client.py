"""Singleton Neo4j driver (same pattern as the Qdrant/embedding singletons
in rag-service and the DB singleton in incident-service)."""
from neo4j import GraphDatabase

from app.config import settings


class Neo4jSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
            )
        return cls._instance

    def close(self):
        self.driver.close()


neo4j_db = Neo4jSingleton()
