/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Aptos", "Inter", "Segoe UI", "sans-serif"],
        body: ["Aptos", "Inter", "Segoe UI", "sans-serif"],
      },
      colors: {
        ink: "#0A0E1A",
        panel: "#111729",
        panel2: "#161D33",
        hair: "rgba(148,163,255,0.14)",
        iris: "#6C5CE7",
        iris2: "#38BDF8",
        teal: "#2DD4BF",
      },
      boxShadow: {
        glow: "0 0 60px -10px rgba(108,92,231,0.45)",
      },
    },
  },
  plugins: [],
};
