"use client";

import LoginForm from "@/components/login-form";
import { AppShell } from "@/components/app-shell";

export default function LoginPage() {
  return (
    <AppShell>
      <div className="max-w-md mx-auto mt-24 p-6 bg-white/80 rounded-lg shadow-lg">
        <h1 className="text-2xl font-semibold mb-4">Sign in</h1>
        <LoginForm />
      </div>
    </AppShell>
  );
}
