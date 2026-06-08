import { BrainCircuit } from "lucide-react";

import type { MemoryItem } from "@/lib/types";

export function MemoryPanel({ memories }: { memories: MemoryItem[] }) {
  return (
    <section id="memory-vault" className="rounded-md border border-[var(--line)] bg-panel/95 p-4 shadow-soft">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <BrainCircuit size={18} aria-hidden="true" />
          <h2 className="text-base font-semibold">Memory Vault</h2>
        </div>
        <span className="text-xs font-medium text-[var(--muted)]">{memories.length} pinned</span>
      </div>
      <div className="space-y-3">
        {memories.map((memory) => (
          <article key={memory.id} className="rounded-md border border-[var(--line)] bg-white p-3">
            <div className="flex items-center justify-between gap-3">
              <span className="rounded bg-tide px-2 py-1 text-xs font-semibold text-white">{memory.type}</span>
              <span className="text-xs text-[var(--muted)]">{Math.round(memory.importance * 100)}%</span>
            </div>
            <p className="mt-3 text-sm leading-6">{memory.content}</p>
            <p className="mt-2 text-xs text-[var(--muted)]">{memory.source}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
