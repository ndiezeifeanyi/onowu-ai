from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentDefinition:
    agent_id: str
    name: str
    description: str
    capabilities: list[str]
    queue: str = "agents"


@dataclass
class AgentContext:
    user_id: str
    goal: str
    conversation_id: str | None = None
    workflow_id: str | None = None
    memories: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    agent_id: str
    output: str
    confidence: float = 0.75
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    memory_writes: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    definition: AgentDefinition

    @abstractmethod
    async def run(self, context: AgentContext) -> AgentResult:
        """Execute an agent against a goal and context."""

    def score_goal(self, goal: str) -> float:
        goal_l = goal.lower()
        matches = sum(1 for capability in self.definition.capabilities if capability in goal_l)
        return matches / max(len(self.definition.capabilities), 1)

