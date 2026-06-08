"use client";

import { AppShell } from "@/components/app-shell";
import { HoverButton } from "@/components/ui/hover-button";
import { LayoutDashboard, BookOpen, MessageSquare } from "lucide-react";

export default function Home() {
  return (
    <AppShell>
      <div className="min-h-screen flex items-center justify-center px-6 py-16">
        <div className="w-full max-w-3xl rounded-2xl bg-gradient-to-br from-white/6 to-white/3 p-10 backdrop-blur-md border border-white/8">
          <div className="text-center">
            <h1 className="text-4xl font-extrabold tracking-tight text-white">Personal AI OS</h1>
            <p className="mt-3 text-lg text-white/80 max-w-2xl mx-auto">
              A compact, professional workspace for multi-agent orchestration — focused, fast, and delightful.
            </p>
          </div>

          <div className="mt-8 flex items-center justify-center gap-4">
            <HoverButton className="flex items-center gap-3 rounded-full px-6 py-3 bg-white/6 text-white" onClick={() => window.location.href = '/api/v1/chat'}>
              <MessageSquare size={18} />
              Talk to Master Agent
            </HoverButton>

            <HoverButton className="flex items-center gap-3 rounded-full px-6 py-3 bg-white/6 text-white" onClick={() => window.open('/api/v1/docs', '_blank')}>
              <LayoutDashboard size={18} />
              API Docs
            </HoverButton>

            <HoverButton className="flex items-center gap-3 rounded-full px-6 py-3 bg-white/6 text-white" onClick={() => window.location.href = '/workflows'}>
              <BookOpen size={18} />
              Workflows
            </HoverButton>
          </div>

          <p className="mt-6 text-center text-sm text-white/60">Focused UI — removed noisy panels for clarity. Use the sidebar for navigation.</p>
        </div>
      </div>
    </AppShell>
  );
}
