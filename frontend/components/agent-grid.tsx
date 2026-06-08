import { Bot, CircleDot, DatabaseZap, RadioTower } from "lucide-react";

import type { Agent } from "@/lib/types";
import { cn } from "@/lib/utils";

const tone = {
  running: "bg-moss text-white",
  queued: "bg-brass text-ink",
  idle: "bg-white text-ink",
  offline: "bg-clay text-white"
};

export function AgentGrid({ agents }: { agents: Agent[] }) {
  return (
    <section id="agent-mesh" className="rounded-md border border-[var(--line)] bg-panel/95 p-4 shadow-soft">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Bot size={18} aria-hidden="true" />
          <h2 className="text-base font-semibold">Agent Mesh</h2>
        </div>
        <RadioTower size={18} className="text-moss" aria-hidden="true" />
      </div>
      <div className="grid gap-3 md:grid-cols-2">
        {agents.map((agent) => (
          <article key={agent.agent_id} className="rounded-md border border-[var(--line)] bg-white p-3">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <h3 className="truncate text-sm font-semibold">{agent.name}</h3>
                <p className="mt-1 line-clamp-2 text-xs leading-5 text-[var(--muted)]">{agent.description}</p>
              </div>
              <span className={cn("rounded px-2 py-1 text-xs font-semibold", tone[agent.status])}>
                {agent.status}
              </span>
            </div>
            <div className="mt-3 flex items-center gap-2 text-xs text-[var(--muted)]">
              <DatabaseZap size={14} aria-hidden="true" />
              <span>{agent.queue}</span>
              <CircleDot size={10} aria-hidden="true" />
              <span>{agent.capabilities.slice(0, 3).join(", ")}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
