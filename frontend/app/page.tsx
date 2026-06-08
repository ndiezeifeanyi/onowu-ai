"use client";

import { AppShell } from "@/components/app-shell";
import BackgroundPaths from "@/components/background-paths";
import SplineScene from "@/components/spline-scene";

export default function Home() {
  const SPLINE_SCENE = ""; // optional: add a Spline scene URL here

  return (
    <AppShell>
      <div className="relative">
        <BackgroundPaths title={"Personal AI OS"} />

        {SPLINE_SCENE && (
          <div className="pointer-events-none absolute right-8 top-24 w-[420px] h-[320px] hidden lg:block">
            <SplineScene scene={SPLINE_SCENE} className="w-full h-full rounded-lg shadow-xl" />
          </div>
        )}
      </div>
    </AppShell>
  );
}
