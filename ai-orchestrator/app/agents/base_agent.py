from abc import ABC, abstractmethod

from app.graph.state import AgentState


class BaseAgent(ABC):
    """
    Abstract base class for all SentinelX agents.
    Every agent must implement the run() method.
    """

    @abstractmethod
    def run(self, state: AgentState) -> AgentState:
        """
        Process the current AgentState and return
        the updated AgentState.
        """
        pass