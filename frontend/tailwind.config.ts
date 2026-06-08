import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1b1f24",
        panel: "#f7f7f2",
        moss: "#496a4a",
        clay: "#a64f3c",
        brass: "#b8892d",
        tide: "#266d78"
      },
      boxShadow: {
        soft: "0 10px 30px rgba(27, 31, 36, 0.08)"
      }
    }
  },
  plugins: [require("@tailwindcss/forms")]
};

export default config;

