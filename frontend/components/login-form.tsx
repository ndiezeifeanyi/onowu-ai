"use client";

import { useState } from "react";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  async function handlePasswordLogin(e: React.FormEvent) {
    e.preventDefault();
    setMessage(null);
    const res = await fetch("/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      setMessage("Logged in");
    } else {
      setMessage("Invalid credentials");
    }
  }

  async function handleRequestCode(e: React.FormEvent) {
    e.preventDefault();
    setMessage(null);
    const res = await fetch("/api/v1/auth/request-code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    if (res.ok) setMessage("Code sent to your email");
    else setMessage("Failed to request code");
  }

  async function handleVerifyCode(e: React.FormEvent) {
    e.preventDefault();
    setMessage(null);
    const res = await fetch("/api/v1/auth/verify-code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, code }),
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      setMessage("Logged in via code");
    } else {
      setMessage("Invalid code");
    }
  }

  function handleGoogle() {
    // open Google OAuth flow handled by backend
    window.location.href = "/api/v1/auth/google/login";
  }

  return (
    <div className="space-y-4">
      {message && <div className="text-sm text-gray-700">{message}</div>}

      <form onSubmit={handlePasswordLogin} className="space-y-2">
        <input
          className="w-full border px-3 py-2 rounded"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="w-full border px-3 py-2 rounded"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="w-full bg-blue-600 text-white py-2 rounded" type="submit">
          Sign in
        </button>
      </form>

      <div className="border-t pt-3">
        <form onSubmit={handleRequestCode} className="flex gap-2">
          <input
            className="flex-1 border px-3 py-2 rounded"
            placeholder="Email for code"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button className="bg-gray-700 text-white px-3 rounded" type="submit">
            Request Code
          </button>
        </form>

        <form onSubmit={handleVerifyCode} className="mt-2 flex gap-2">
          <input
            className="flex-1 border px-3 py-2 rounded"
            placeholder="Enter code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <button className="bg-green-600 text-white px-3 rounded" type="submit">
            Verify
          </button>
        </form>
      </div>

      <div className="pt-3">
        <button onClick={handleGoogle} className="w-full border py-2 rounded">
          Continue with Google
        </button>
      </div>
    </div>
  );
}
