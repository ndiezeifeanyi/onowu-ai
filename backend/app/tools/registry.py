from app.core.prompt_guard import detect_prompt_injection
from app.core.security import has_role
from app.tools.base import BaseTool, ToolContext, ToolResult
from app.tools.implementations import (
    BrowserAutomationTool,
    EmailTool,
    FileIndexTool,
    NotificationTool,
    ResearchSearchTool,
    ScholarshipSourcesTool,
    SemanticMemoryTool,
    WeatherTool,
)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> BaseTool:
        return self._tools[tool_id]

    def list_tools(self) -> list[BaseTool]:
        return list(self._tools.values())


class PermissionedToolExecutor:
    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or build_default_tool_registry()

    async def execute(self, tool_id: str, context: ToolContext) -> ToolResult:
        tool = self.registry.get(tool_id)
        if tool.requires_approval and not has_role(context.role, {"owner", "admin"}):
            return ToolResult(
                tool_id=tool_id,
                success=False,
                error="Tool requires owner or admin approval.",
            )
        markers: list[str] = []
        for value in context.input.values():
            if isinstance(value, str):
                markers.extend(detect_prompt_injection(value))
        if markers:
            return ToolResult(
                tool_id=tool_id,
                success=False,
                output={"markers": markers},
                error="Potential prompt-injection content detected.",
            )
        return await tool.execute(context)


def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    for tool in (
        ScholarshipSourcesTool(),
        ResearchSearchTool(),
        WeatherTool(),
        NotificationTool(),
        EmailTool(),
        BrowserAutomationTool(),
        SemanticMemoryTool(),
        FileIndexTool(),
    ):
        registry.register(tool)
    return registry

