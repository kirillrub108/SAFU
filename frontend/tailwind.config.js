/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'lecture': '#28a745',
        'practice': '#ffc107',
        'lab': '#17a2b8',
        'attestation': '#dc3545',
      },
    },
  },
  plugins: [],
}

