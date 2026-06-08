import asyncio
import json
from collections.abc import AsyncGenerator

import redis.asyncio as redis

from app.core.config import get_settings


class WorkflowEventService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _channel(self, workflow_id: str) -> str:
        return f"workflow-events:{workflow_id}"

    async def publish(self, workflow_id: str, event: dict) -> None:
        client = redis.from_url(self.settings.redis_url, decode_responses=True)
        try:
            await client.publish(self._channel(workflow_id), json.dumps(event))
        finally:
            await client.aclose()

    async def stream(self, workflow_id: str) -> AsyncGenerator[str, None]:
        client = redis.from_url(self.settings.redis_url, decode_responses=True)
        pubsub = client.pubsub()
        try:
            await pubsub.subscribe(self._channel(workflow_id))
            yield "event: connected\ndata: {}\n\n"
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=15)
                if message and message.get("data"):
                    yield f"event: workflow\ndata: {message['data']}\n\n"
                else:
                    yield "event: heartbeat\ndata: {}\n\n"
                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(self._channel(workflow_id))
            await pubsub.aclose()
            await client.aclose()

