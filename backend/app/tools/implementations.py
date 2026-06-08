from app.core.config import get_settings
from app.tools.base import BaseTool, ToolContext, ToolDefinition, ToolResult


class ScholarshipSourcesTool(BaseTool):
    definition = ToolDefinition(
        tool_id="scholarship_sources",
        name="Scholarship Sources",
        description="Returns configured scholarship sources and ranking hints.",
        capabilities=["scholarship", "funding", "deadline", "university portals"],
        risk_level="low",
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        fields = context.input.get("fields", [])
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={
                "fields": fields,
                "sources": [
                    {"name": "DAAD", "type": "official"},
                    {"name": "Erasmus Mundus", "type": "official"},
                    {"name": "Chevening", "type": "official"},
                    {"name": "Commonwealth", "type": "official"},
                    {"name": "ScholarshipPortal", "type": "aggregator"},
                    {"name": "FindAMasters", "type": "aggregator"},
                ],
                "ranking_weights": {
                    "funding": 0.4,
                    "eligibility": 0.25,
                    "deadline": 0.25,
                    "program_fit": 0.1,
                },
            },
        )


class ResearchSearchTool(BaseTool):
    definition = ToolDefinition(
        tool_id="research_search",
        name="Research Search",
        description="Searches research providers through API adapters.",
        capabilities=["arxiv", "semantic scholar", "pubmed", "research"],
        risk_level="low",
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={
                "providers": ["arxiv", "semantic_scholar", "pubmed"],
                "query": context.input,
                "status": "adapter-ready",
            },
        )


class WeatherTool(BaseTool):
    definition = ToolDefinition(
        tool_id="weather",
        name="Weather",
        description="Fetches weather information from configured providers.",
        capabilities=["weather", "forecast", "alerts"],
        risk_level="low",
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        settings = get_settings()
        providers = {
            "openweather": bool(settings.openweather_api_key),
            "weatherapi": bool(settings.weatherapi_key),
            "tomorrow": bool(settings.tomorrow_api_key),
        }
        configured = [name for name, active in providers.items() if active]
        if not configured:
            return ToolResult(
                tool_id=self.tool_id,
                success=False,
                output={"configured_providers": []},
                error="No weather provider API key is configured.",
            )
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={"configured_providers": configured, "input": context.input},
        )


class NotificationTool(BaseTool):
    definition = ToolDefinition(
        tool_id="notification",
        name="Notification",
        description="Queues dashboard/email/mobile notification payloads.",
        capabilities=["notification", "alert", "dashboard"],
        risk_level="medium",
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={"delivery": "queued", "payload": context.input},
        )


class EmailTool(BaseTool):
    definition = ToolDefinition(
        tool_id="email",
        name="Email",
        description="Sends email through configured SMTP credentials.",
        capabilities=["email", "smtp"],
        risk_level="high",
        requires_approval=True,
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        settings = get_settings()
        if not settings.smtp_host or not settings.smtp_username:
            return ToolResult(
                tool_id=self.tool_id,
                success=False,
                output={},
                error="SMTP credentials are not configured.",
            )
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={"status": "ready", "from": settings.smtp_from},
        )


class BrowserAutomationTool(BaseTool):
    definition = ToolDefinition(
        tool_id="browser_automation",
        name="Browser Automation",
        description="Runs Playwright browser automation jobs with approval policies.",
        capabilities=["playwright", "browser", "scraping", "forms"],
        risk_level="high",
        requires_approval=True,
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={"status": "job-ready", "goal": context.input.get("goal")},
        )


class SemanticMemoryTool(BaseTool):
    definition = ToolDefinition(
        tool_id="semantic_memory",
        name="Semantic Memory",
        description="Searches vector-backed user memory.",
        capabilities=["memory", "vector", "semantic search"],
        risk_level="low",
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={"query": context.input.get("query"), "status": "service-backed"},
        )


class FileIndexTool(BaseTool):
    definition = ToolDefinition(
        tool_id="file_index",
        name="File Index",
        description="Indexes approved workspace files without escaping sandbox boundaries.",
        capabilities=["file", "pdf", "spreadsheet", "document"],
        risk_level="medium",
    )

    async def execute(self, context: ToolContext) -> ToolResult:
        return ToolResult(
            tool_id=self.tool_id,
            success=True,
            output={"scope": context.input.get("scope", "approved_workspace"), "status": "ready"},
        )

