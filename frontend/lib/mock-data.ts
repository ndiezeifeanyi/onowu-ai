import type { Agent, IntelligenceItem, MemoryItem, NotificationItem, Workflow } from "./types";

export const agents: Agent[] = [
  {
    agent_id: "master",
    name: "Master Agent",
    description: "Central orchestration, planning, delegation, evaluation, and memory coordination.",
    capabilities: ["planning", "delegation", "evaluation"],
    status: "running",
    queue: "agents"
  },
  {
    agent_id: "scholarship",
    name: "Scholarship Agent",
    description: "Global MSc opportunity monitoring, ranking, deadline tracking, and summaries.",
    capabilities: ["DAAD", "Erasmus", "funding", "deadlines"],
    status: "queued",
    queue: "scholarships"
  },
  {
    agent_id: "research",
    name: "Research Agent",
    description: "ArXiv, Semantic Scholar, and PubMed research intelligence.",
    capabilities: ["papers", "summaries", "trends"],
    status: "idle",
    queue: "research"
  },
  {
    agent_id: "weather",
    name: "Weather Agent",
    description: "Forecasts, alerts, travel, and schedule recommendations.",
    capabilities: ["forecast", "alerts"],
    status: "idle",
    queue: "agents"
  }
];

export const workflows: Workflow[] = [
  {
    id: "wf-msc-scholarships",
    goal: "Rank MSc scholarships in AI, Data Science, Bioinformatics, and Microbiology",
    status: "running",
    priority: 8,
    updated_at: "Today 09:35",
    agent: "Scholarship Agent"
  },
  {
    id: "wf-daily-briefing",
    goal: "Generate daily productivity, research, scholarship, and reminder briefing",
    status: "planning",
    priority: 6,
    updated_at: "Today 08:00",
    agent: "Reporting Agent"
  },
  {
    id: "wf-literature-monitor",
    goal: "Monitor AI and bioinformatics research trends",
    status: "completed",
    priority: 5,
    updated_at: "Yesterday 20:10",
    agent: "Research Agent"
  }
];

export const scholarships: IntelligenceItem[] = [
  {
    title: "Erasmus Mundus Joint Master in AI",
    source: "Erasmus Mundus",
    url: "https://erasmus-plus.ec.europa.eu/opportunities/opportunities-for-individuals/students/erasmus-mundus-joint-masters",
    score: 92,
    deadline: "2027-01-10",
    tags: ["full funding", "Europe", "AI"]
  },
  {
    title: "DAAD MSc Data Science Funding",
    source: "DAAD",
    url: "https://www.daad.de/en/studying-in-germany/scholarships/daad-scholarships/",
    score: 86,
    deadline: "2026-11-30",
    tags: ["Germany", "Data Science", "stipend"]
  },
  {
    title: "Commonwealth Shared Scholarship",
    source: "Commonwealth",
    url: "https://cscuk.fcdo.gov.uk/scholarships/commonwealth-shared-scholarships/",
    score: 79,
    deadline: "2026-12-12",
    tags: ["UK", "full funding", "eligibility review"]
  }
];

export const researchItems: IntelligenceItem[] = [
  {
    title: "Foundation models for single-cell bioinformatics",
    source: "Semantic Scholar",
    url: "https://www.semanticscholar.org/",
    score: 89,
    tags: ["bioinformatics", "foundation models"]
  },
  {
    title: "Efficient retrieval-augmented agents for scientific discovery",
    source: "arXiv",
    url: "https://arxiv.org/",
    score: 84,
    tags: ["agents", "RAG", "research workflows"]
  },
  {
    title: "Machine learning for antimicrobial resistance prediction",
    source: "PubMed",
    url: "https://pubmed.ncbi.nlm.nih.gov/",
    score: 81,
    tags: ["microbiology", "ML", "public health"]
  }
];

export const memories: MemoryItem[] = [
  {
    id: "mem-1",
    type: "preference",
    content: "Prioritize MSc scholarships in AI, Data Science, Bioinformatics, and Microbiology.",
    source: "onboarding",
    importance: 0.92
  },
  {
    id: "mem-2",
    type: "goal",
    content: "Deploy the production system to Google Cloud Europe.",
    source: "architecture",
    importance: 0.88
  },
  {
    id: "mem-3",
    type: "workflow",
    content: "Use Ollama fallback when external LLM providers are unavailable.",
    source: "offline-mode",
    importance: 0.74
  }
];

export const notifications: NotificationItem[] = [
  {
    id: "note-1",
    title: "Scholarship scan queued",
    body: "The scholarship queue is tracking six priority sources.",
    status: "pending",
    created_at: "Today 09:35"
  },
  {
    id: "note-2",
    title: "Research monitor updated",
    body: "Three high-fit research trends were added to the briefing queue.",
    status: "sent",
    created_at: "Yesterday 20:10"
  }
];
