"use client";

import {
  Bot,
  Database,
  FlaskConical,
  GraduationCap,
  LayoutDashboard,
  Workflow
} from "lucide-react";

import { HoverButton } from "@/components/ui/hover-button";

const navItems = [
  { label: "Overview", icon: LayoutDashboard, target: "overview" },
  { label: "Master Agent", icon: Bot, target: "master-agent" },
  { label: "Workflow Queue", icon: Workflow, target: "workflow-queue" },
  { label: "Scholarship Scanner", icon: GraduationCap, target: "scholarship-intelligence" },
  { label: "Research Monitor", icon: FlaskConical, target: "research-intelligence" },
  { label: "Memory Vault", icon: Database, target: "memory-vault" }
];

export function AppShell({ children }: Readonly<{ children: React.ReactNode }>) {
  function goToSection(target: string) {
    document.getElementById(target)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <main className="app-backdrop min-h-screen lg:grid lg:grid-cols-[232px_1fr]">
      <aside className="border-b border-white/10 bg-ink/95 text-white shadow-[8px_0_40px_rgba(10,12,16,0.18)] lg:min-h-screen lg:border-b-0 lg:border-r">
        <div className="flex h-20 items-center gap-3 px-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-md bg-brass text-ink">
            <Bot size={20} aria-hidden="true" />
          </div>
          <div>
            <p className="text-sm font-semibold leading-5">Personal AI OS</p>
            <p className="text-xs text-white/62">Autonomous command layer</p>
          </div>
        </div>
        <nav className="flex gap-2 overflow-x-auto px-3 pb-3 lg:block lg:space-y-2 lg:overflow-visible">
          {navItems.map((item) => (
            <HoverButton
              key={item.label}
              className="h-10 min-w-max rounded-md bg-white/[0.06] px-3 py-2 text-sm text-white/80 hover:text-white lg:w-full lg:justify-start"
              type="button"
              title={item.label}
              onClick={() => goToSection(item.target)}
            >
              <item.icon size={17} aria-hidden="true" />
              <span>{item.label}</span>
            </HoverButton>
          ))}
        </nav>
        <div className="hidden px-5 pt-6 lg:block">
          <div className="rounded-md border border-white/10 bg-white/[0.04] p-3">
            <p className="text-xs font-semibold uppercase text-brass">Mode</p>
            <p className="mt-2 text-sm leading-5 text-white/78">Private multi-agent workspace</p>
          </div>
        </div>
      </aside>
      <section className="min-w-0">{children}</section>
    </main>
  );
}
