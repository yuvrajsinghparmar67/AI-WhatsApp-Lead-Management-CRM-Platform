/**
 * Design token system for the CRM.
 *
 * "brand" is a deep indigo-to-violet identity (distinct from generic
 * blue-SaaS defaults), "surface" gives us layered light/dark neutrals for
 * the glassmorphism panels, and the type scale/shadows/radii below are
 * referenced everywhere in the UI instead of ad-hoc Tailwind values -
 * this is what keeps the "premium SaaS" look consistent as the app grows.
 */
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f2f1fd",
          100: "#e6e4fb",
          200: "#c3bdf5",
          300: "#a096ee",
          400: "#7a6ce6",
          500: "#5b4bdc",
          600: "#4736c2",
          700: "#382a99",
          800: "#292070",
          900: "#1a1547",
        },
        surface: {
          light: "#fafafa",
          card: "#ffffff",
          dark: "#0d0d12",
          "dark-card": "#17171f",
        },
      },
      fontFamily: {
        display: ["'Sora'", "system-ui", "sans-serif"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
      },
      borderRadius: {
        xl2: "1.25rem",
      },
      boxShadow: {
        soft: "0 8px 30px rgba(26, 21, 71, 0.08)",
        "soft-dark": "0 8px 30px rgba(0, 0, 0, 0.35)",
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};
