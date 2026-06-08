import { AgentGrid } from "@/components/agent-grid";
import { AppShell } from "@/components/app-shell";
import { ChatPanel } from "@/components/chat-panel";
import { CommandActions } from "@/components/command-actions";
import { IntelligencePanels } from "@/components/intelligence-panels";
import { MemoryPanel } from "@/components/memory-panel";
import { OperationsPanel } from "@/components/operations-panel";
import { StatStrip } from "@/components/stat-strip";
import { WorkflowBoard } from "@/components/workflow-board";
import { agents, memories, notifications, researchItems, scholarships, workflows } from "@/lib/mock-data";

const statusTiles = [
  { label: "Region", value: "GCP europe-west1" },
  { label: "Model layer", value: "OpenAI + Ollama" },
  { label: "Access", value: "Private RBAC" }
];

export default function Home() {
  return (
    <AppShell>
      <div className="mx-auto max-w-[1500px] px-4 py-5 sm:px-6 lg:px-8">
        <section
          id="overview"
          className="mb-5 overflow-hidden rounded-md border border-white/55 bg-white/72 p-5 shadow-soft backdrop-blur-xl lg:p-7"
        >
          <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_420px] xl:items-end">
            <div>
              <p className="text-sm font-semibold uppercase text-clay">Autonomous operating layer</p>
              <h1 className="mt-2 max-w-4xl text-4xl font-semibold tracking-normal text-ink lg:text-5xl">
                Personal AI OS command center
              </h1>
              <p className="mt-4 max-w-3xl text-base leading-7 text-[var(--muted)]">
                Multi-agent orchestration, scholarship intelligence, research monitoring, persistent memory,
                scheduling, and secure task execution in one private workspace.
              </p>
              <div className="mt-5">
                <CommandActions />
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-3 xl:grid-cols-1">
              {statusTiles.map((tile) => (
                <div key={tile.label} className="rounded-md border border-[var(--line)] bg-panel/90 p-4">
                  <p className="text-xs font-semibold uppercase text-[var(--muted)]">{tile.label}</p>
                  <p className="mt-2 text-lg font-semibold text-ink">{tile.value}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <div className="space-y-4">
          <StatStrip />

          <div className="grid gap-4 xl:grid-cols-[minmax(420px,0.92fr)_minmax(0,1.08fr)]">
            <ChatPanel />
            <WorkflowBoard workflows={workflows} />
          </div>

          <IntelligencePanels scholarships={scholarships} researchItems={researchItems} />

          <div className="grid gap-4 xl:grid-cols-[minmax(360px,0.82fr)_minmax(0,1.18fr)]">
            <MemoryPanel memories={memories} />
            <AgentGrid agents={agents} />
          </div>

          <OperationsPanel notifications={notifications} />
        </div>
      </div>
    </AppShell>
  );
}
