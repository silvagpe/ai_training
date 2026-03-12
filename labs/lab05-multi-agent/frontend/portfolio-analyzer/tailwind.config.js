/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#de3341',
          dark: '#b22834',
          soft: 'rgb(255, 255, 255)',
          softer: 'rgba(222, 51, 65, 0.06)',
          border: '#f3b2b8',
          text: '#7b1f27',
        },
        status: {
          buy: '#10b981',
          hold: '#f59e0b',
          sell: '#f43f5e',
        },
      },
    },
  },
  plugins: [],
}
