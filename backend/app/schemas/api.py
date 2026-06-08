from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.db.models import (
    MemoryType,
    NotificationStatus,
    RoleName,
    ScheduleStatus,
    TaskStatus,
    WorkflowStatus,
)


class APIError(BaseModel):
    detail: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None
    timezone: str = "Africa/Lagos"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str | None
    role: RoleName
    is_active: bool
    timezone: str
    preferences: dict[str, Any]
    created_at: datetime


class ChatSessionCreate(BaseModel):
    title: str | None = None


class ChatSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    summary: str | None = None
    created_at: datetime
    updated_at: datetime


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1)


class ChatMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime


class AgentRead(BaseModel):
    agent_id: str
    name: str
    description: str
    capabilities: list[str]


class AgentRunRequest(BaseModel):
    goal: str = Field(min_length=3)
    context: dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    agent_id: str
    output: str
    confidence: float
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    memory_writes: list[str] = Field(default_factory=list)


class WorkflowCreate(BaseModel):
    goal: str = Field(min_length=3)
    priority: int = Field(default=5, ge=1, le=10)
    metadata: dict[str, Any] = Field(default_factory=dict)
    enqueue: bool = True


class WorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    goal: str
    status: WorkflowStatus
    priority: int
    plan: list[dict[str, Any]]
    result: dict[str, Any]
    error: str | None
    created_at: datetime
    updated_at: datetime


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workflow_id: str | None
    name: str
    queue: str
    status: TaskStatus
    priority: int
    attempts: int
    max_retries: int
    result: dict[str, Any]
    error: str | None
    created_at: datetime
    updated_at: datetime


class MemoryCreate(BaseModel):
    memory_type: MemoryType = MemoryType.note
    content: str = Field(min_length=1)
    source: str = "manual"
    importance: float = Field(default=0.5, ge=0, le=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    memory_type: MemoryType
    content: str
    source: str
    importance: float
    metadata_json: dict[str, Any]
    created_at: datetime


class MemorySearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    memory_type: MemoryType | None = None


class ToolRead(BaseModel):
    tool_id: str
    name: str
    description: str
    capabilities: list[str]
    risk_level: str
    requires_approval: bool


class ToolExecuteRequest(BaseModel):
    input: dict[str, Any] = Field(default_factory=dict)


class ToolExecuteResponse(BaseModel):
    tool_id: str
    success: bool
    output: dict[str, Any]
    error: str | None = None


class ScheduleCreate(BaseModel):
    name: str
    cron: str
    workflow_goal: str
    timezone: str = "Africa/Lagos"
    payload: dict[str, Any] = Field(default_factory=dict)


class ScheduleUpdate(BaseModel):
    status: ScheduleStatus | None = None
    cron: str | None = None
    payload: dict[str, Any] | None = None


class ScheduleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    cron: str
    timezone: str
    workflow_goal: str
    status: ScheduleStatus
    next_run_at: datetime | None
    created_at: datetime


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    channel: str
    title: str
    body: str
    status: NotificationStatus
    created_at: datetime


class ReportGenerateRequest(BaseModel):
    report_type: str = "daily"
    title: str | None = None
    source_window: str = "24h"


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    report_type: str
    title: str
    summary: str | None
    content: str
    created_at: datetime

