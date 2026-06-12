import { BrainCircuit } from "lucide-react";

import type { MemoryItem } from "@/lib/types";

export function MemoryPanel({ memories }: { memories: MemoryItem[] }) {
  return (
    <section id="memory-vault" className="rounded-md border border-white/10 bg-ink text-white p-4 shadow-soft">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <BrainCircuit size={18} aria-hidden="true" />
          <h2 className="text-base font-semibold">Memory Vault</h2>
        </div>
        <span className="text-xs font-medium text-white/60">{memories.length} pinned</span>
      </div>
      <div className="space-y-3">
        {memories.map((memory) => (
          <article key={memory.id} className="rounded-md border border-white/10 bg-white/10 p-3">
            <div className="flex items-center justify-between gap-3">
              <span className="rounded bg-tide px-2 py-1 text-xs font-semibold text-white">{memory.type}</span>
              <span className="text-xs text-white/60">{Math.round(memory.importance * 100)}%</span>
            </div>
            <p className="mt-3 text-sm leading-6 text-white">{memory.content}</p>
            <p className="mt-2 text-xs text-white/60">{memory.source}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
