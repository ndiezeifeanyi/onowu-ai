"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { AtSignIcon, ChevronLeftIcon, Grid2x2PlusIcon, AppleIcon, GithubIcon } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

export function AuthPage() {
  const [email, setEmail] = useState('');
  const [codeRequested, setCodeRequested] = useState(false);
  const [code, setCode] = useState('');
  const [message, setMessage] = useState<string | null>(null);

  const [consent, setConsent] = useState(false);

  async function requestCode() {
    setMessage(null);
    if (!consent) {
      setMessage('You must agree to Terms of Service and Privacy Policy');
      return;
    }
    try {
      const res = await fetch('/api/v1/auth/request-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) throw new Error('request failed');
      setCodeRequested(true);
      setMessage('Code sent to your email');
    } catch (err) {
      setMessage('Failed to request code');
    }
  }

  async function verifyCode() {
    setMessage(null);
    try {
      const res = await fetch('/api/v1/auth/verify-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, code }),
      });
      if (!res.ok) throw new Error('invalid');
      const data = await res.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      setMessage('Signed in');
      // redirect to home
      window.location.href = '/';
    } catch (err) {
      setMessage('Invalid code');
    }
  }

  function handleGoogle() {
    window.location.href = '/api/v1/auth/google/login';
  }

  return (
    <main className="relative md:h-screen md:overflow-hidden lg:grid lg:grid-cols-2">
      <div className="bg-muted/60 relative hidden h-full flex-col border-r p-10 lg:flex">
        <div className="from-background absolute inset-0 z-10 bg-gradient-to-t to-transparent" />
        <div className="z-10 flex items-center gap-2">
          <Grid2x2PlusIcon className="size-6" />
          <p className="text-xl font-semibold">Asme</p>
        </div>
        <div className="z-10 mt-auto">
          <blockquote className="space-y-2">
            <p className="text-xl">
              &ldquo;This Platform has helped me to save time and serve my
              clients faster than ever before.&rdquo;
            </p>
            <footer className="font-mono text-sm font-semibold">~ Ali Hassan</footer>
          </blockquote>
        </div>
        <div className="absolute inset-0">
          {/* Decorative paths handled by BackgroundPaths on homepage */}
        </div>
      </div>
      <div className="relative flex min-h-screen flex-col justify-center p-4">
        <div
          aria-hidden
          className="absolute inset-0 isolate contain-strict -z-10 opacity-60"
        >
          <div className="bg-[radial-gradient(68.54%_68.72%_at_55.02%_31.46%,--theme(--color-foreground/.06)_0,hsla(0,0%,55%,.02)_50%,--theme(--color-foreground/.01)_80%)] absolute top-0 right-0 h-320 w-140 -translate-y-87.5 rounded-full" />
          <div className="bg-[radial-gradient(50%_50%_at_50%_50%,--theme(--color-foreground/.04)_0,--theme(--color-foreground/.01)_80%,transparent_100%)] absolute top-0 right-0 h-320 w-60 [translate:5%_-50%] rounded-full" />
          <div className="bg-[radial-gradient(50%_50%_at_50%_50%,--theme(--color-foreground/.04)_0,--theme(--color-foreground/.01)_80%,transparent_100%)] absolute top-0 right-0 h-320 w-60 -translate-y-87.5 rounded-full" />
        </div>
        <div className="mx-auto space-y-4 sm:w-sm">
          <div className="flex items-center gap-2 lg:hidden">
            <Grid2x2PlusIcon className="size-6" />
            <p className="text-xl font-semibold">Asme</p>
          </div>
          <div className="flex flex-col space-y-1">
            <h1 className="font-heading text-2xl font-bold tracking-wide">Sign In or Join Now!</h1>
            <p className="text-muted-foreground text-base">login or create your asme account.</p>
          </div>

          <div className="space-y-2">
            <Button type="button" size="lg" className="w-full" onClick={handleGoogle}>
              <span className="me-2">Continue with Google</span>
            </Button>
            <Button type="button" size="lg" className="w-full">
              <span className="me-2">Continue with Apple</span>
            </Button>
            <Button type="button" size="lg" className="w-full">
              <span className="me-2">Continue with GitHub</span>
            </Button>
          </div>

          <div className="flex items-center">
            <div className="flex-1 h-px bg-border" />
            <span className="px-3 text-sm text-muted-foreground">OR</span>
            <div className="flex-1 h-px bg-border" />
          </div>

          <div className="space-y-2">
            <p className="text-muted-foreground text-start text-xs">Enter your email address to sign in or create an account</p>
            <div className="relative h-max">
              <Input placeholder="your.email@example.com" className="peer ps-9" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
              <div className="text-muted-foreground pointer-events-none absolute inset-y-0 start-0 flex items-center justify-center ps-3 peer-disabled:opacity-50">
                <AtSignIcon className="size-4" aria-hidden="true" />
              </div>
            </div>

            {!codeRequested ? (
                <>
                  <div className="flex items-center gap-2">
                    <input id="consent" type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
                    <label htmlFor="consent" className="text-sm text-muted-foreground">I agree to the Terms of Service and Privacy Policy</label>
                  </div>
                  <Button type="button" className="w-full" onClick={requestCode}>
                    <span>Continue With Email</span>
                  </Button>
                </>
              ) : (
              <div className="space-y-2">
                <Input placeholder="Enter code" value={code} onChange={(e) => setCode(e.target.value)} />
                <Button type="button" className="w-full" onClick={verifyCode}>Verify Code</Button>
              </div>
            )}
          </div>

          {message && <div className="text-sm text-gray-700">{message}</div>}

          <p className="text-muted-foreground mt-8 text-sm">
            By clicking continue, you agree to our{' '}
            <a href="#" className="hover:text-primary underline underline-offset-4">Terms of Service</a>{' '}
            and{' '}
            <a href="#" className="hover:text-primary underline underline-offset-4">Privacy Policy</a>.
          </p>
        </div>
      </div>
    </main>
  );
}

export default AuthPage;
