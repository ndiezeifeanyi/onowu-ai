import { Bell, CheckCircle2, FileText, ShieldCheck } from "lucide-react";

import type { NotificationItem } from "@/lib/types";

export function OperationsPanel({ notifications }: { notifications: NotificationItem[] }) {
  return (
    <section className="rounded-md border border-white/10 bg-ink text-white p-4 shadow-soft">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-base font-semibold">Operations</h2>
        <ShieldCheck size={18} className="text-moss" aria-hidden="true" />
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        <div className="rounded-md border border-white/10 bg-white/10 p-3">
          <FileText size={18} className="text-tide" aria-hidden="true" />
          <p className="mt-3 text-sm font-semibold">Daily report</p>
          <p className="mt-1 text-xs text-[var(--muted)]">Queued at 08:00</p>
        </div>
        <div className="rounded-md border border-white/10 bg-white/10 p-3">
          <Bell size={18} className="text-brass" aria-hidden="true" />
          <p className="mt-3 text-sm font-semibold">Notifications</p>
          <p className="mt-1 text-xs text-white/60">{notifications.length} recent</p>
        </div>
        <div className="rounded-md border border-white/10 bg-white/10 p-3">
          <CheckCircle2 size={18} className="text-moss" aria-hidden="true" />
          <p className="mt-3 text-sm font-semibold">Audit trail</p>
          <p className="mt-1 text-xs text-[var(--muted)]">RBAC enforced</p>
        </div>
      </div>
      <div className="mt-4 space-y-3">
        {notifications.map((notification) => (
          <article key={notification.id} className="rounded-md border border-white/10 bg-white/10 p-3">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="text-sm font-semibold">{notification.title}</h3>
                <p className="mt-1 text-xs leading-5 text-white/60">{notification.body}</p>
              </div>
              <span className="rounded border border-white/10 bg-white/10 px-2 py-1 text-xs">
                {notification.status}
              </span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

