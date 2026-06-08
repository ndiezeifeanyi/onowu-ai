"use client";

import {
  Bot,
  Database,
  GraduationCap,
  LayoutDashboard,
  Workflow
} from "lucide-react";

import { HoverButton } from "@/components/ui/hover-button";

const navItems = [
  { label: "Overview", icon: LayoutDashboard, target: "overview" },
  { label: "Workflows", icon: Workflow, target: "workflow-queue" },
  { label: "Agents", icon: Bot, target: "master-agent" },
];

export function AppShell({ children }: Readonly<{ children: React.ReactNode }>) {
  function goToSection(target: string) {
    document.getElementById(target)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <main className="app-backdrop min-h-screen bg-gradient-to-br from-sky-900 via-indigo-900 to-rose-900 text-white lg:grid lg:grid-cols-[96px_1fr]">
      <aside className="border-b border-white/6 bg-white/6/10 text-white shadow-[8px_0_40px_rgba(10,12,16,0.18)] lg:min-h-screen lg:border-b-0 lg:border-r">
        <div className="flex h-20 items-center gap-3 px-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-md bg-brass text-ink">
            <Bot size={20} aria-hidden="true" />
          </div>
        </div>
        <nav className="flex flex-col gap-2 px-2 pb-3">
          {navItems.map((item) => (
            <HoverButton
              key={item.label}
              className="h-12 w-12 rounded-md bg-white/[0.04] p-2 text-sm text-white/90 flex items-center justify-center"
              type="button"
              title={item.label}
              onClick={() => goToSection(item.target)}
            >
              <item.icon size={18} aria-hidden="true" />
            </HoverButton>
          ))}
        </nav>
      </aside>
      <section className="min-w-0">{children}</section>
    </main>
  );
}
