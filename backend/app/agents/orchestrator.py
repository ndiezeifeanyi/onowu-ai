from typing import Any, TypedDict

from app.agents.base import AgentContext, AgentResult
from app.agents.registry import AgentRegistry, build_default_agent_registry


class WorkflowState(TypedDict, total=False):
    user_id: str
    goal: str
    metadata: dict[str, Any]
    plan: list[dict[str, Any]]
    agent_results: list[dict[str, Any]]
    final: dict[str, Any]


class MasterAgent:
    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self.registry = registry or build_default_agent_registry()

    def plan(self, goal: str) -> list[dict[str, Any]]:
        selected = self.registry.select_for_goal(goal)
        return [
            {
                "step": "classify_goal",
                "agent_id": "master",
                "description": "Classify intent, risks, required tools, and memory needs.",
            },
            {
                "step": "delegate",
                "agent_id": selected.definition.agent_id,
                "description": f"Delegate execution to {selected.definition.name}.",
            },
            {
                "step": "evaluate",
                "agent_id": "master",
                "description": "Evaluate output, retry if needed, and persist useful memory.",
            },
        ]

    async def run(self, context: AgentContext) -> AgentResult:
        selected = self.registry.select_for_goal(context.goal)
        result = await selected.run(context)
        output = (
            f"Master Agent delegated this goal to {selected.definition.name}. "
            f"{result.output}"
        )
        return AgentResult(
            agent_id="master",
            output=output,
            confidence=result.confidence,
            tool_calls=result.tool_calls,
            memory_writes=result.memory_writes,
            artifacts={
                "selected_agent": selected.definition.agent_id,
                "delegate_artifacts": result.artifacts,
                "plan": self.plan(context.goal),
            },
        )


class WorkflowOrchestrator:
    def __init__(self, master_agent: MasterAgent | None = None) -> None:
        self.master_agent = master_agent or MasterAgent()

    async def execute(self, context: AgentContext) -> dict[str, Any]:
        plan = self.master_agent.plan(context.goal)
        result = await self.master_agent.run(context)
        return {
            "plan": plan,
            "result": {
                "output": result.output,
                "confidence": result.confidence,
                "tool_calls": result.tool_calls,
                "memory_writes": result.memory_writes,
                "artifacts": result.artifacts,
            },
        }

    def graph_available(self) -> bool:
        try:
            import langgraph  # noqa: F401
        except ImportError:
            return False
        return True

