import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/app/**/*.{ts,tsx}", "./src/components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          900: "#012340",
          700: "#142273",
          600: "#343BBF",
          500: "#3C36D9",
          950: "#011140",
          accent: "#43D9CA"
        }
      }
    }
  },
  plugins: []
};

export default config;
