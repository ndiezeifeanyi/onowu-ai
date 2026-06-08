import { Activity, Cpu, LockKeyhole, Server, Waypoints } from "lucide-react";

const stats = [
  { label: "Active workflows", value: "3", icon: Waypoints, tone: "text-tide" },
  { label: "Agents online", value: "11", icon: Cpu, tone: "text-moss" },
  { label: "Memory items", value: "128", icon: Server, tone: "text-clay" },
  { label: "Security posture", value: "RBAC", icon: LockKeyhole, tone: "text-ink" },
  { label: "Offline fallback", value: "Ollama", icon: Activity, tone: "text-tide" }
];

export function StatStrip() {
  return (
    <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
      {stats.map((stat) => (
        <div key={stat.label} className="rounded-md border border-[var(--line)] bg-white/82 p-4 shadow-soft">
          <div className="flex items-center justify-between gap-3">
            <p className="text-xs font-medium uppercase text-[var(--muted)]">{stat.label}</p>
            <stat.icon className={stat.tone} size={18} aria-hidden="true" />
          </div>
          <p className="mt-3 text-2xl font-semibold text-ink">{stat.value}</p>
        </div>
      ))}
    </section>
  );
}
