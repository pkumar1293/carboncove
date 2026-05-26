import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#1B5E20', light: '#388E3C', dark: '#1B5E20' },
        accent: { DEFAULT: '#00897B' },
        surface: { DEFAULT: '#F1F8F2' },
      }
    },
  },
  plugins: [],
}
export default config
