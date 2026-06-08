from app.agents.base import AgentContext, AgentDefinition, AgentResult, BaseAgent


class ResearchAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="research",
        name="Research Agent",
        description="Searches, compares, summarizes, and monitors research literature.",
        capabilities=["research", "papers", "arxiv", "semantic scholar", "pubmed", "literature"],
        queue="research",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        topics = context.metadata.get("topics") or ["AI", "Data Science", "Bioinformatics"]
        output = (
            "Research workflow prepared: search arXiv, Semantic Scholar, and PubMed; "
            "deduplicate papers; summarize findings; compare methods; store research notes."
        )
        return AgentResult(
            agent_id=self.definition.agent_id,
            output=output,
            confidence=0.82,
            tool_calls=[
                {"tool_id": "research_search", "input": {"topics": topics, "limit": 10}},
                {"tool_id": "semantic_memory", "input": {"query": context.goal}},
            ],
            memory_writes=[f"Research interest captured: {', '.join(topics)}"],
            artifacts={"topics": topics, "sources": ["arxiv", "semantic_scholar", "pubmed"]},
        )


class ScholarshipAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="scholarship",
        name="Scholarship Agent",
        description="Monitors, ranks, and summarizes MSc scholarship opportunities.",
        capabilities=[
            "scholarship",
            "msc",
            "daad",
            "erasmus",
            "chevening",
            "commonwealth",
            "funding",
            "deadline",
        ],
        queue="scholarships",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        fields = context.metadata.get("fields") or [
            "AI",
            "Machine Learning",
            "Data Science",
            "Bioinformatics",
            "Microbiology",
        ]
        output = (
            "Scholarship workflow prepared: scan priority sources, normalize opportunities, "
            "detect duplicates, analyze eligibility, rank by funding/deadline/fit, and notify."
        )
        return AgentResult(
            agent_id=self.definition.agent_id,
            output=output,
            confidence=0.88,
            tool_calls=[
                {"tool_id": "scholarship_sources", "input": {"fields": fields}},
                {"tool_id": "semantic_memory", "input": {"query": "previously liked scholarships"}},
            ],
            memory_writes=[f"Scholarship fields tracked: {', '.join(fields)}"],
            artifacts={
                "ranking_weights": {"funding": 0.4, "deadline": 0.25, "eligibility": 0.25, "fit": 0.1},
                "sources": [
                    "DAAD",
                    "Erasmus Mundus",
                    "Chevening",
                    "Commonwealth",
                    "ScholarshipPortal",
                    "FindAMasters",
                ],
            },
        )


class ReportingAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="reporting",
        name="Reporting Agent",
        description="Generates daily, weekly, productivity, scholarship, and research reports.",
        capabilities=["report", "summary", "daily", "weekly", "briefing", "productivity"],
        queue="reports",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output=(
                "Report workflow prepared: collect recent workflows, tasks, memories, scholarships, "
                "research notes, and reminders into a concise briefing."
            ),
            confidence=0.8,
            tool_calls=[{"tool_id": "notification", "input": {"channel": "dashboard"}}],
            memory_writes=["Reporting preference updated from latest request."],
            artifacts={"report_sections": ["priorities", "scholarships", "research", "reminders"]},
        )


class SchedulerAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="scheduler",
        name="Scheduler Agent",
        description="Creates recurring tasks, reminders, cron workflows, and proactive triggers.",
        capabilities=["schedule", "reminder", "recurring", "cron", "automation", "trigger"],
        queue="default",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output="Scheduling workflow prepared with cron validation, next-run tracking, and worker dispatch.",
            confidence=0.78,
            tool_calls=[],
            memory_writes=["Scheduling intent captured."],
        )


class WeatherAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="weather",
        name="Weather Agent",
        description="Provides weather alerts, predictions, and schedule recommendations.",
        capabilities=["weather", "forecast", "travel", "rain", "temperature", "alert"],
        queue="agents",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output=(
                "Weather workflow prepared: query configured providers, evaluate alerts, "
                "and produce schedule/travel recommendations."
            ),
            confidence=0.76,
            tool_calls=[{"tool_id": "weather", "input": context.metadata}],
            memory_writes=["Weather preference updated."],
        )


class NotificationAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="notification",
        name="Notification Agent",
        description="Routes dashboard, email, and future mobile notifications.",
        capabilities=["notify", "notification", "email", "alert", "message"],
        queue="notifications",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output="Notification workflow prepared with dashboard-first delivery and email fallback.",
            confidence=0.77,
            tool_calls=[{"tool_id": "notification", "input": {"title": "AI OS update"}}],
        )


class EmailAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="email",
        name="Email Agent",
        description="Composes and sends email through configured SMTP providers.",
        capabilities=["email", "smtp", "inbox", "send mail", "message"],
        queue="notifications",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output="Email workflow prepared; delivery requires SMTP credentials in environment secrets.",
            confidence=0.72,
            tool_calls=[{"tool_id": "email", "input": {"subject": context.goal}}],
        )


class FileManagementAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="file_management",
        name="File Management Agent",
        description="Indexes and manages approved local files with sandbox-aware policies.",
        capabilities=["file", "document", "pdf", "spreadsheet", "folder", "filesystem"],
        queue="agents",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output="File workflow prepared with sandbox checks and approved workspace-only operations.",
            confidence=0.74,
            tool_calls=[{"tool_id": "file_index", "input": {"scope": "approved_workspace"}}],
        )


class WebAutomationAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="web_automation",
        name="Web Automation Agent",
        description="Uses Playwright for website interaction, scraping, and monitoring.",
        capabilities=["browser", "playwright", "scrape", "web automation", "form"],
        queue="browser",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output="Browser automation workflow prepared with Playwright and permission-gated actions.",
            confidence=0.75,
            tool_calls=[{"tool_id": "browser_automation", "input": {"goal": context.goal}}],
        )


class MemoryAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="memory",
        name="Memory Agent",
        description="Stores, retrieves, consolidates, and audits long-term and semantic memory.",
        capabilities=["memory", "remember", "recall", "preference", "history"],
        queue="agents",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output="Memory workflow prepared: classify, store, embed, and retrieve user-scoped memories.",
            confidence=0.84,
            tool_calls=[{"tool_id": "semantic_memory", "input": {"query": context.goal}}],
            memory_writes=[context.goal],
        )


class LearningRecommendationAgent(BaseAgent):
    definition = AgentDefinition(
        agent_id="learning_recommendation",
        name="Learning/Recommendation Agent",
        description="Recommends learning paths, opportunities, and next actions from user history.",
        capabilities=["learn", "recommend", "course", "progress", "skill", "next action"],
        queue="agents",
    )

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.definition.agent_id,
            output="Recommendation workflow prepared using goals, memory, research trends, and deadlines.",
            confidence=0.79,
            tool_calls=[{"tool_id": "semantic_memory", "input": {"query": context.goal}}],
            memory_writes=["Learning recommendation request captured."],
        )

