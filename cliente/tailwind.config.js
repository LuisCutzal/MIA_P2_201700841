/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors:{
        danger:"#ef1761",
        warning:"#d38d3f",
        primary:"#262626",
        second:"#985ee4",
        third:"#6032eb",
      },
    },
  },
  plugins: [],
}
