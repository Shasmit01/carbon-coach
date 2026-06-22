/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0F6D3B",
        secondary: "#2BAE66",
        accent: "#8BC34A",
        background: "#F5FFF6",
        "text-dark": "#1F2937",
        "text-light": "#6B7280",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
      backgroundImage: {
        "gradient-primary": "linear-gradient(135deg, #0F6D3B 0%, #2BAE66 100%)",
        "gradient-accent": "linear-gradient(135deg, #8BC34A 0%, #2BAE66 100%)",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
  ],
}
