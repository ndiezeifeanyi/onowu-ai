"use client";

import { useState } from "react";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [agreed, setAgreed] = useState(false);

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
    window.location.href = "/api/v1/auth/google/login";
  }

  function handleApple() {
    window.location.href = "/api/v1/auth/apple/login";
  }

  function handleGitHub() {
    window.location.href = "/api/v1/auth/github/login";
  }

  return (
    <div className="space-y-4 w-full max-w-sm relative z-50 pointer-events-auto">
      
      {message && <div className="text-sm text-gray-800 bg-gray-100 p-2 rounded border border-gray-200">{message}</div>}

      {/* Buttons Fixed: High contrast borders and dark text explicitly overrides transparency */}
      <div className="space-y-2">
        <button 
          type="button"
          onClick={handleGoogle} 
          className="w-full bg-white hover:bg-gray-50 text-gray-900 font-medium py-2.5 px-4 rounded-xl text-sm transition-colors block text-center border-2 border-gray-300 shadow-sm"
        >
          Continue with Google
        </button>

        <button 
          type="button"
          onClick={handleApple} 
          className="w-full bg-black hover:bg-zinc-800 text-white font-medium py-2.5 px-4 rounded-xl text-sm transition-colors block text-center border border-black shadow-sm"
        >
          Continue with Apple
        </button>

        <button 
          type="button"
          onClick={handleGitHub} 
          className="w-full bg-zinc-900 hover:bg-zinc-800 text-white font-medium py-2.5 px-4 rounded-xl text-sm transition-colors block text-center border border-zinc-900 shadow-sm"
        >
          Continue with GitHub
        </button>
      </div>

      <div className="text-center my-4 text-xs text-gray-500 font-bold tracking-wider">OR</div>

      {/* Input Form Fields */}
      <div className="space-y-3">
        <div>
          <label className="text-xs font-semibold text-gray-700 block mb-1">
            Enter your email address to sign in or create an account
          </label>
          <input
            className="w-full border-2 border-gray-300 px-3 py-2.5 rounded-lg text-sm text-black focus:outline-none focus:ring-2 focus:ring-black focus:border-black bg-white"
            placeholder="ndiezeifeanyi@gmail.com"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        {/* Checkbox Agreement Layout */}
        <div className="flex items-start gap-2 py-1">
          <input 
            type="checkbox" 
            id="terms" 
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
            className="mt-0.5 h-4 w-4 rounded border-gray-300 accent-black cursor-pointer"
          />
          <label htmlFor="terms" className="text-xs text-gray-600 leading-normal cursor-pointer select-none">
            I agree to the <span className="underline font-medium text-gray-900">Terms of Service</span> and <span className="underline font-medium text-gray-900">Privacy Policy</span>.
          </label>
        </div>

        {/* Continue With Email Button Fixed: Changed text-gray-400 to text-white for visibility */}
        <form onSubmit={handleRequestCode}>
          <button 
            type="submit" 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-xl text-sm shadow-sm transition-colors"
          >
            Continue With Email
          </button>
        </form>
      </div>

      {/* Code validation segment */}
      <div className="border-t border-gray-200 pt-3 mt-2">
        <form onSubmit={handleVerifyCode} className="flex gap-2">
          <input
            className="flex-1 border-2 border-gray-300 px-3 py-2 rounded-lg text-sm text-black bg-white focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Enter verification code"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <button className="bg-gray-900 hover:bg-black text-white px-4 rounded-lg text-sm font-medium transition-colors" type="submit">
            Verify
          </button>
        </form>
      </div>

    </div>
  );
}