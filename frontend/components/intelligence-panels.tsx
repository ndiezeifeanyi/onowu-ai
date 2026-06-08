"use client";

import { ExternalLink, FlaskConical, GraduationCap, TrendingUp } from "lucide-react";

import { HoverButton } from "@/components/ui/hover-button";
import type { IntelligenceItem } from "@/lib/types";

function IntelligenceList({
  title,
  id,
  icon: Icon,
  items
}: {
  title: string;
  id: string;
  icon: typeof GraduationCap;
  items: IntelligenceItem[];
}) {
  return (
    <section id={id} className="rounded-md border border-[var(--line)] bg-white/86 p-4 shadow-soft">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Icon size={18} aria-hidden="true" />
          <h2 className="text-base font-semibold">{title}</h2>
        </div>
        <TrendingUp size={18} className="text-moss" aria-hidden="true" />
      </div>
      <div className="space-y-3">
        {items.map((item) => (
          <article key={`${item.source}-${item.title}`} className="rounded-md border border-[var(--line)] bg-panel/95 p-3">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="text-sm font-semibold">{item.title}</h3>
                <p className="mt-1 text-xs text-[var(--muted)]">
                  {item.source}
                  {item.deadline ? ` - ${item.deadline}` : ""}
                </p>
              </div>
              <div className="flex shrink-0 items-center gap-2">
                <span className="rounded bg-moss px-2 py-1 text-xs font-semibold text-white">{item.score}</span>
                <HoverButton
                  className="h-8 w-8 rounded-md bg-white px-0 py-0 text-ink"
                  type="button"
                  title={`Open ${item.source}`}
                  onClick={() => window.open(item.url, "_blank", "noopener,noreferrer")}
                >
                  <ExternalLink size={14} aria-hidden="true" />
                </HoverButton>
              </div>
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              {item.tags.map((tag) => (
                <span key={tag} className="rounded border border-[var(--line)] bg-white px-2 py-1 text-xs text-ink">
                  {tag}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export function IntelligencePanels({
  scholarships,
  researchItems
}: {
  scholarships: IntelligenceItem[];
  researchItems: IntelligenceItem[];
}) {
  return (
    <div className="grid gap-4 xl:grid-cols-2">
      <IntelligenceList
        id="scholarship-intelligence"
        title="Scholarship Intelligence"
        icon={GraduationCap}
        items={scholarships}
      />
      <IntelligenceList
        id="research-intelligence"
        title="Research Intelligence"
        icon={FlaskConical}
        items={researchItems}
      />
    </div>
  );
}
