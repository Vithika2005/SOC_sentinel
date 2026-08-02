from app.graph.builder import graph
from app.graph.state import create_initial_state


class PipelineService:
    """
    Service responsible for executing the LangGraph pipeline.
    """

    @staticmethod
    def execute(incident: dict) -> dict:
        """
        Execute the complete LangGraph pipeline.

        Args:
            incident: Incident received from API or Kafka.

        Returns:
            Final pipeline output.
        """

        state = create_initial_state(incident)

        result = graph.invoke(state)

        return result