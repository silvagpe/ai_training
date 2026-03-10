import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/app/**/*.{ts,tsx}", "./src/components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          900: "#012340",
          800: "#025939",
          700: "#027333",
          500: "#03A63C",
          400: "#04D939"
        }
      }
    }
  },
  plugins: []
};

export default config;
