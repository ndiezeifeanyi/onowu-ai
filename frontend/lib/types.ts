export type Agent = {
  agent_id: string;
  name: string;
  description: string;
  capabilities: string[];
  status: "idle" | "running" | "queued" | "offline";
  queue: string;
};

export type Workflow = {
  id: string;
  goal: string;
  status: "pending" | "planning" | "running" | "waiting" | "completed" | "failed" | "cancelled";
  priority: number;
  updated_at: string;
  agent: string;
};

export type IntelligenceItem = {
  title: string;
  source: string;
  url: string;
  score: number;
  deadline?: string;
  tags: string[];
};

export type NotificationItem = {
  id: string;
  title: string;
  body: string;
  status: "pending" | "sent" | "failed" | "read";
  created_at: string;
};

export type MemoryItem = {
  id: string;
  type: string;
  content: string;
  source: string;
  importance: number;
};
