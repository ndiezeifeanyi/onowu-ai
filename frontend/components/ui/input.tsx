"use client";

import * as React from "react";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

export const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className = "", ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={["w-full border px-3 py-2 rounded bg-transparent text-current", className].join(" ")}
      {...props}
    />
  );
});

Input.displayName = "Input";

export default Input;
