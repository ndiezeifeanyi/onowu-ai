const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export type ApiOptions = {
  token?: string;
};

async function request<T>(path: string, init: RequestInit = {}, options: ApiOptions = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  if (options.token) {
    headers.set("Authorization", `Bearer ${options.token}`);
  }
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
    cache: "no-store"
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string; refresh_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    }),
  createWorkflow: (goal: string, token: string) =>
    request("/workflows", { method: "POST", body: JSON.stringify({ goal, enqueue: true }) }, { token }),
  listAgents: (token: string) => request("/agents", {}, { token }),
  searchMemory: (query: string, token: string) =>
    request("/memory/search", { method: "POST", body: JSON.stringify({ query }) }, { token })
};

