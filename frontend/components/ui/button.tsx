"use client";

import * as React from "react";

export type ButtonVariant = "ghost" | "primary" | "default";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  children: React.ReactNode;
}

export function Button({ variant = "default", className = "", children, ...props }: ButtonProps) {
  const base = "inline-flex items-center justify-center rounded-[1.15rem] px-4 py-2 font-semibold";
  const variantClass =
    variant === "ghost"
      ? "bg-white/95 dark:bg-black/95 text-black dark:text-white"
      : variant === "primary"
      ? "bg-brass text-ink"
      : "bg-white/10 text-white";

  return (
    <button {...props} className={`${base} ${variantClass} ${className}`.trim()}>
      {children}
    </button>
  );
}

export default Button;
