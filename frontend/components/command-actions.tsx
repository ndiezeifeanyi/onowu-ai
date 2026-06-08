"use client";

import { BookOpen, Bot, GraduationCap, RadioTower } from "lucide-react";

import { HoverButton } from "@/components/ui/hover-button";

function scrollToSection(target: string) {
  document.getElementById(target)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function CommandActions() {
  return (
    <div className="flex flex-wrap gap-3">
      <HoverButton
        className="bg-ink px-5 py-2.5 text-sm text-white"
        type="button"
        onClick={() => scrollToSection("master-agent")}
      >
        <Bot size={16} aria-hidden="true" />
        Talk to Master Agent
      </HoverButton>
      <HoverButton
        className="bg-white/76 px-5 py-2.5 text-sm"
        type="button"
        onClick={() => scrollToSection("scholarship-intelligence")}
      >
        <GraduationCap size={16} aria-hidden="true" />
        Scholarship Scanner
      </HoverButton>
      <HoverButton
        className="bg-white/76 px-5 py-2.5 text-sm"
        type="button"
        onClick={() => scrollToSection("research-intelligence")}
      >
        <RadioTower size={16} aria-hidden="true" />
        Research Monitor
      </HoverButton>
      <HoverButton
        className="bg-white/76 px-5 py-2.5 text-sm"
        type="button"
        onClick={() => window.open("http://127.0.0.1:8000/docs", "_blank", "noopener,noreferrer")}
      >
        <BookOpen size={16} aria-hidden="true" />
        API Docs
      </HoverButton>
    </div>
  );
}
