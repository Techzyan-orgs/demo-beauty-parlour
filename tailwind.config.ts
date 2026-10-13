import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          50: '#fbf8ed',
          100: '#f6eed4',
          200: '#eedba9',
          300: '#e3c275',
          400: '#d9a944',
          500: '#c59127',
          600: '#ab741d',
          700: '#89551a',
          800: '#71441c',
          900: '#5f391b',
          accent: '#D4AF37',
          light: '#F5E6BE',
          dark: '#997B24',
        },
        luxe: {
          black: '#0A0A0C',
          dark: '#121216',
          card: '#18181F',
          muted: '#24242E',
          border: '#32323D',
          cream: '#FAF7F2',
          sand: '#F3ECE1',
          champagne: '#E8DCB8',
          rose: '#E5B4B0',
          terracotta: '#C86D51',
          bronze: '#B38B59',
        },
      },
      fontFamily: {
        serif: ['var(--font-playfair)', 'Cormorant Garamond', 'Georgia', 'serif'],
        sans: ['var(--font-sans)', 'Plus Jakarta Sans', 'Inter', 'sans-serif'],
      },
      backgroundImage: {
        'radial-gradient': 'radial-gradient(var(--tw-gradient-stops))',
        'gold-shimmer': 'linear-gradient(135deg, #ECC880 0%, #D4AF37 50%, #997B24 100%)',
        'dark-glass': 'linear-gradient(180deg, rgba(24, 24, 31, 0.75) 0%, rgba(18, 18, 22, 0.90) 100%)',
        'light-glass': 'linear-gradient(180deg, rgba(255, 255, 255, 0.85) 0%, rgba(243, 236, 225, 0.90) 100%)',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
        marquee: {
          '0%': { transform: 'translateX(0%)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        marquee: 'marquee 25s linear infinite',
      },
    },
  },
  plugins: [],
};

export default config;
