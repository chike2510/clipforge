import type { Config } from 'tailwindcss';
const config: Config = { content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'], theme: { extend: { colors: { ink: '#17211b', cream: '#f4f1e8', moss: '#a8c5a0', coral: '#ee7657', lime: '#d4e98b' }, fontFamily: { display: ['var(--font-display)'], sans: ['var(--font-sans)'] } } }, plugins: [] };
export default config;
