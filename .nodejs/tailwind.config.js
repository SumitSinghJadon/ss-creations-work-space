/** @type {import('tailwindcss').Config} */


module.exports = {
  content: [
    "../assets/static/js/knox-form.js",
    "../apps/IS_Nexus/templates/new/*.html",
    "../apps/IS_Nexus/templates/new/components/*.html",
    "../projects/Sampling/AccessArmor/templates/dashboard.html",
    "../projects/Sampling/EntryForms/templates/new/*.html",
    "../projects/**/**/templates/new/*.html",
    "../projects/**/**/templates/new/*.html"
  ],
  
  daisyui: {
    themes: [
      "corporate",
      "light",
      "dark",
      "cupcake",
      "bumblebee",
      "emerald",
      "synthwave",
      "retro",
      "cyberpunk",
      "valentine",
      "halloween",
      "garden",
      "forest",
      "aqua",
      "lofi",
      "pastel",
      "fantasy",
      "wireframe",
      "black",
      "luxury",
      "dracula",
      "cmyk",
      "autumn",
      "business",
      "acid",
      "lemonade",
      "night",
      "coffee",
      "winter",
      "dim",
      "nord",
      "sunset",
    ],
  },
  plugins: [require("daisyui")],
}

