"use client";

import { Send, Sparkles } from "lucide-react";
import { useState } from "react";

import { HoverButton } from "@/components/ui/hover-button";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Master Agent is ready. Current focus: scholarships, research monitoring, daily reports, and deployment readiness."
    }
  ]);
  const [draft, setDraft] = useState("");

  function submit() {
    const value = draft.trim();
    if (!value) return;
    setMessages((current) => [
      ...current,
      { role: "user", content: value },
      {
        role: "assistant",
        content: "Workflow accepted. I will classify the goal, select agents and tools, then persist useful memory."
      }
    ]);
    setDraft("");
  }

  return (
    <section
      id="master-agent"
      className="flex min-h-[460px] flex-col rounded-md border border-white/10 bg-ink text-white shadow-soft"
    >
      <div className="flex h-14 items-center justify-between border-b border-white/10 px-4">
        <div className="flex items-center gap-2">
          <Sparkles size={18} className="text-brass" aria-hidden="true" />
          <h2 className="text-base font-semibold">Master Agent</h2>
        </div>
        <span className="rounded bg-moss px-2 py-1 text-xs font-semibold">online</span>
      </div>
      <div className="scrollbar-thin flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={message.role === "user" ? "ml-auto max-w-[88%]" : "mr-auto max-w-[92%]"}
          >
            <p
              className={
                message.role === "user"
                  ? "rounded-md bg-brass px-3 py-2 text-sm leading-6 text-ink"
                  : "rounded-md bg-white/9 px-3 py-2 text-sm leading-6 text-white/88"
              }
            >
              {message.content}
            </p>
          </div>
        ))}
      </div>
      <div className="flex gap-2 border-t border-white/10 p-3">
        <textarea
          className="min-h-11 flex-1 resize-none rounded-md border-0 bg-white px-3 py-2 text-sm text-ink outline-none ring-0"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              submit();
            }
          }}
          aria-label="Message"
        />
        <HoverButton
          className="h-11 w-11 shrink-0 rounded-md bg-brass px-0 py-0 text-ink"
          type="button"
          onClick={submit}
          title="Send"
        >
          <Send size={18} aria-hidden="true" />
        </HoverButton>
      </div>
    </section>
  );
}
