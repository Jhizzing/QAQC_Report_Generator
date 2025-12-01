/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // LogiQore Brand Colors (Refined Slate/Midnight Theme)
                primary: {
                    DEFAULT: '#F59E0B', // Amber-500 (Vibrant Gold)
                    light: '#FBBF24',   // Amber-400
                    dark: '#D97706',    // Amber-600
                    glow: 'rgba(245, 158, 11, 0.5)', // Amber Glow
                },
                secondary: {
                    DEFAULT: '#334155', // Slate-700
                    light: '#475569',   // Slate-600
                    dark: '#1E293B',    // Slate-800
                },
                accent: {
                    DEFAULT: '#0EA5E9', // Sky-500 (Subtle Cool Accent)
                    light: '#38BDF8',   // Sky-400
                    dark: '#0284C7',    // Sky-600
                },
                surface: {
                    DEFAULT: '#1E293B', // Slate-800 (Card Background)
                    light: '#334155',   // Slate-700 (Hover State)
                    dark: '#0F172A',    // Slate-900 (Deep Surface)
                    glass: 'rgba(30, 41, 59, 0.7)', // Glassmorphism
                },
                background: {
                    DEFAULT: '#0F172A', // Slate-900 (Main Background)
                    light: '#F1F5F9',   // Slate-100 (Light Mode)
                    dark: '#020617',    // Slate-950 (Deepest Dark)
                },
                status: {
                    success: '#10B981', // Emerald-500
                    warning: '#F59E0B', // Amber-500
                    error: '#EF4444',   // Red-500
                    info: '#3B82F6',    // Blue-500
                }
            },
            fontFamily: {
                sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'hero-glow': 'conic-gradient(from 180deg at 50% 50%, #111827 0deg, #1F2937 50%, #111827 100%)',
            }
        },
    },
    plugins: [],
    darkMode: 'class',
};
