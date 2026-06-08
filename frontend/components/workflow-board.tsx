import { CheckCircle2, CircleDashed, OctagonAlert, PauseCircle, PlayCircle } from "lucide-react";

import type { Workflow } from "@/lib/types";
import { cn } from "@/lib/utils";

const statusIcon = {
  pending: CircleDashed,
  planning: CircleDashed,
  running: PlayCircle,
  waiting: PauseCircle,
  completed: CheckCircle2,
  failed: OctagonAlert,
  cancelled: PauseCircle
};

const statusTone = {
  pending: "border-tide/40 text-tide",
  planning: "border-brass/50 text-brass",
  running: "border-moss/60 text-moss",
  waiting: "border-brass/50 text-brass",
  completed: "border-moss/60 text-moss",
  failed: "border-clay/60 text-clay",
  cancelled: "border-ink/30 text-ink"
};

export function WorkflowBoard({ workflows }: { workflows: Workflow[] }) {
  return (
    <section id="workflow-queue" className="rounded-md border border-[var(--line)] bg-white/86 p-4 shadow-soft">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-base font-semibold">Workflow Queue</h2>
        <span className="text-xs font-medium text-[var(--muted)]">{workflows.length} tracked</span>
      </div>
      <div className="space-y-3">
        {workflows.map((workflow) => {
          const Icon = statusIcon[workflow.status];
          return (
            <article
              key={workflow.id}
              className={cn("rounded-md border-l-4 bg-panel/95 p-3", statusTone[workflow.status])}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <h3 className="text-sm font-semibold text-ink">{workflow.goal}</h3>
                  <p className="mt-1 text-xs text-[var(--muted)]">
                    {workflow.agent} - priority {workflow.priority} - {workflow.updated_at}
                  </p>
                </div>
                <Icon size={18} aria-hidden="true" />
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
