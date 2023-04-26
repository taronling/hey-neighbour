/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "website/**/*.{html, css, js}",
    "users/**/*.{html, css, js}",
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

