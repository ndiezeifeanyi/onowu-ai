export async function streamAgentCognition(
  objective: string,
  onEvent: (event: any) => void
): Promise<void> {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const response = await fetch(`${API_BASE}/agents/run_stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ goal: objective }),
  });

  if (!response.ok || !response.body) {
    throw new Error("Failed to instantiate downstream Agentic OS session pipeline.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let searchBuffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    searchBuffer += decoder.decode(value, { stream: true });
    const components = searchBuffer.split("\n\n");
    searchBuffer = components.pop() || "";

    for (const line of components) {
      if (line.startsWith("data: ")) {
        try {
          const structuralData = JSON.parse(line.replace("data: ", ""));
          onEvent(structuralData);
        } catch (err) {
          // ignore malformed chunks
        }
      }
    }
  }
}
