"use client";

import { useMemo, useEffect, useState } from "react";
import { motion } from "framer-motion";

function FloatingPaths({ position }: { position: number }) {
    const paths = useMemo(() => {
        return Array.from({ length: 36 }, (_, i) => ({
            id: i,
            d: `M-${380 - i * 5 * position} -${189 + i * 6}C-${
                380 - i * 5 * position
            } -${189 + i * 6} -${312 - i * 5 * position} ${216 - i * 6} ${
                152 - i * 5 * position
            } ${343 - i * 6}C${616 - i * 5 * position} ${470 - i * 6} ${
                684 - i * 5 * position
            } ${875 - i * 6} ${684 - i * 5 * position} ${875 - i * 6}`,
            width: 0.5 + i * 0.03,
        }));
    }, [position]);

    const [isMounted, setIsMounted] = useState(false);
    useEffect(() => {
        setIsMounted(true);
    }, []);

    return (
        <div className="absolute inset-0 pointer-events-none">
            <svg
                className="w-full h-full text-slate-950 dark:text-white"
                viewBox="0 0 696 316"
                fill="none"
                preserveAspectRatio="xMidYMid slice"
            >
                <title>Background Paths</title>
                {paths.map((path) => (
                    <motion.path
                        key={path.id}
                        d={path.d}
                        stroke="currentColor"
                        strokeWidth={path.width}
                        strokeOpacity={0.1 + path.id * 0.03}
                        initial={{ pathLength: 0.3, opacity: 0.6 }}
                        animate={{
                            pathLength: 1,
                            opacity: [0.3, 0.6, 0.3],
                            pathOffset: [0, 1, 0],
                        }}
                        transition={{
                            duration: isMounted ? 20 + Math.random() * 10 : 25,
                            repeat: Number.POSITIVE_INFINITY,
                            ease: "linear",
                        }}
                    />
                ))}
            </svg>
        </div>
    );
}

export function BackgroundPaths({
    title = "Personal AI OS",
}: {
    title?: string;
}) {
    const words = useMemo(() => title.split(" "), [title]);

    return (
        <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-white dark:bg-neutral-950">
            <div className="absolute inset-0 z-0">
                <FloatingPaths position={1} />
                <FloatingPaths position={-1} />
            </div>

            <div className="relative z-10 container mx-auto px-4 md:px-6 text-center">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold mb-8 tracking-tighter leading-tight flex flex-wrap justify-center gap-x-4 gap-y-2 text-neutral-900 dark:text-white drop-shadow-[0_6px_18px_rgba(0,0,0,0.25)]">
                        {words.map((word, wordIndex) => (
                            <span key={wordIndex} className="inline-block whitespace-nowrap">
                                {word.split("").map((letter, letterIndex) => (
                                    <span
                                        key={`${wordIndex}-${letterIndex}`}
                                        className="inline-block font-extrabold text-neutral-900 dark:text-white"
                                    >
                                        {letter}
                                    </span>
                                ))}
                            </span>
                        ))}
                    </h1>

                    <div className="inline-block group relative bg-gradient-to-b from-black/10 to-white/10 dark:from-white/10 dark:to-black/10 p-px rounded-2xl backdrop-blur-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
                        <a
                            href="/login"
                            className="inline-flex items-center justify-center rounded-[1.15rem] px-8 py-6 text-lg font-semibold backdrop-blur-md bg-white/95 hover:bg-white/100 dark:bg-black/95 dark:hover:bg-black/100 text-black dark:text-white transition-all duration-300 group-hover:-translate-y-0.5 border border-black/10 dark:border-white/10 hover:shadow-md dark:hover:shadow-neutral-800/50"
                        >
                            <span className="opacity-90 group-hover:opacity-100 transition-opacity">Unlock your digital twin</span>
                            <span className="ml-3 opacity-70 group-hover:opacity-100 group-hover:translate-x-1.5 transition-all duration-300">→</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default BackgroundPaths;
