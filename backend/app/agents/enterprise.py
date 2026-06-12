import json
from typing import Any, AsyncGenerator

from app.ai.providers import ModelRouter


class EnterpriseReActAgent:
    def __init__(self, llm_client: Any, memory_vault: Any, mcp_client: Any):
        self.llm = llm_client
        self.memory = memory_vault
        self.mcp = mcp_client

    async def _get_memory_context(self, user_id: str | None = None) -> str:
        # Attempt to derive a concise memory context from the vector memory provider if available.
        try:
            if hasattr(self.memory, "search") and user_id:
                results = await self.memory.search(user_id=user_id, query="", limit=5)
                return "\n".join(r.get("text", "") for r in results)
        except Exception:
            return ""
        return ""

    async def _append_memory(self, user_id: str | None, event: dict[str, Any]) -> None:
        try:
            if hasattr(self.memory, "upsert") and user_id and isinstance(event, dict):
                await self.memory.upsert(user_id=user_id, item_id=event.get("id", "evt"), text=json.dumps(event), metadata={})
        except Exception:
            return

    async def execute_stream(self, goal: str, user_id: str | None = None) -> AsyncGenerator[dict[str, Any], None]:
        max_loops = 15
        loop_count = 0

        memory_context = await self._get_memory_context(user_id)

        while loop_count < max_loops:
            loop_count += 1
            prompt = (
                "You are an enterprise agent. Produce a JSON object describing the next cognitive step.\n"
                "Return either: {\"type\": \"action\", \"reasoning\": str, \"tool\": str, \"args\": {...}}\n"
                "or: {\"type\": \"final\", \"reasoning\": str, \"output\": {...}}\n"
                f"Goal: {goal}\nMemoryContext: {memory_context}\n"
            )

            llm_resp = await self.llm.complete(prompt)
            reasoning_text = llm_resp.text if hasattr(llm_resp, "text") else str(llm_resp)

            # Attempt to parse LLM output as JSON; fall back to final output text
            try:
                cognition_step = json.loads(reasoning_text)
            except Exception:
                cognition_step = {"type": "final", "reasoning": reasoning_text, "output": reasoning_text}

            yield {"type": "cognition", "step": cognition_step.get("reasoning", "")}

            if cognition_step.get("type") == "action":
                tool = cognition_step.get("tool")
                args = cognition_step.get("args", {})
                yield {"type": "syscall", "tool": tool, "args": args}

                # Execute via MCP client
                try:
                    result = await self.mcp.call(tool, args)
                except Exception as exc:
                    result = {"tool": tool, "status": "error", "error": str(exc)}

                await self._append_memory(user_id, result)
                yield {"type": "observation", "result": result}

            elif cognition_step.get("type") == "final":
                yield {"type": "final_output", "result": cognition_step.get("output")}
                break
