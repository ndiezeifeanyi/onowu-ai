from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolDefinition:
    tool_id: str
    name: str
    description: str
    capabilities: list[str]
    risk_level: str = "low"
    requires_approval: bool = False


@dataclass
class ToolContext:
    user_id: str
    role: str
    input: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    tool_id: str
    success: bool
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class BaseTool(ABC):
    definition: ToolDefinition

    @property
    def tool_id(self) -> str:
        return self.definition.tool_id

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def description(self) -> str:
        return self.definition.description

    @property
    def capabilities(self) -> list[str]:
        return self.definition.capabilities

    @property
    def risk_level(self) -> str:
        return self.definition.risk_level

    @property
    def requires_approval(self) -> bool:
        return self.definition.requires_approval

    @abstractmethod
    async def execute(self, context: ToolContext) -> ToolResult:
        """Run the tool."""

