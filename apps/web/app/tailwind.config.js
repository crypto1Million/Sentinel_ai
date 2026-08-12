/** @type {import('tailwindcss').Config} */

module.exports = {

  content: [

    "./app/**/*.{js,ts,jsx,tsx}",

    "./components/**/*.{js,ts,jsx,tsx}"
  ],

  theme: {

    extend: {

      colors: {

        sentinel: {

          green: "#00ff88",

          dark: "#0d1117"
        }
      }
    }
  },

  plugins: []
}