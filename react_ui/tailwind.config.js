/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // LogiQore Brand Colors
                primary: {
                    DEFAULT: '#FBBF24', // Brand Gold
                    light: '#FCD34D',   // Lighter Gold
                    dark: '#B45309',    // Darker Gold/Amber
                    glow: 'rgba(251, 191, 36, 0.5)', // Gold Glow
                },
                secondary: {
                    DEFAULT: '#1F2937', // Gray-800
                    light: '#374151',   // Gray-700
                    dark: '#111827',    // Brand Dark (Gray-900)
                },
                accent: {
                    DEFAULT: '#F59E0B', // Amber-500
                    light: '#FBBF24',   // Amber-400
                    dark: '#D97706',    // Amber-600
                },
                surface: {
                    DEFAULT: '#1F2937', // Dark surface (Gray-800)
                    light: '#374151',   // Lighter surface
                    dark: '#111827',    // Darker surface (Brand Dark)
                    glass: 'rgba(31, 41, 55, 0.7)', // Glassmorphism
                },
                background: {
                    DEFAULT: '#111827', // Brand Dark
                    light: '#F3F4F6',   // Light mode bg (if needed)
                    dark: '#030712',    // Deepest dark
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
}
