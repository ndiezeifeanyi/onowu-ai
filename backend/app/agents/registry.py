from app.agents.base import BaseAgent
from app.agents.specialized import (
    EmailAgent,
    FileManagementAgent,
    LearningRecommendationAgent,
    MemoryAgent,
    NotificationAgent,
    ReportingAgent,
    ResearchAgent,
    SchedulerAgent,
    ScholarshipAgent,
    WeatherAgent,
    WebAutomationAgent,
)


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.definition.agent_id] = agent

    def get(self, agent_id: str) -> BaseAgent:
        return self._agents[agent_id]

    def list_agents(self) -> list[BaseAgent]:
        return list(self._agents.values())

    def select_for_goal(self, goal: str) -> BaseAgent:
        if not self._agents:
            raise ValueError("No agents registered")
        scored = sorted(
            self._agents.values(),
            key=lambda agent: (agent.score_goal(goal), agent.definition.agent_id),
            reverse=True,
        )
        best = scored[0]
        if best.score_goal(goal) == 0:
            return self._agents["memory"] if "memory" in self._agents else best
        return best


def build_default_agent_registry() -> AgentRegistry:
    registry = AgentRegistry()
    for agent in (
        ResearchAgent(),
        ScholarshipAgent(),
        ReportingAgent(),
        SchedulerAgent(),
        WeatherAgent(),
        NotificationAgent(),
        EmailAgent(),
        FileManagementAgent(),
        WebAutomationAgent(),
        MemoryAgent(),
        LearningRecommendationAgent(),
    ):
        registry.register(agent)
    return registry

