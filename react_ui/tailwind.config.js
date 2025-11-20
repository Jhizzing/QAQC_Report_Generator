/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Geological Theme Colors
                primary: {
                    DEFAULT: '#4A7C59', // Muted forest green
                    light: '#5D9A6E',
                    dark: '#3A6047',
                },
                secondary: {
                    DEFAULT: '#A0714F', // Muted brown
                    light: '#B88A6E',
                    dark: '#8A5F3E',
                },
                accent: {
                    DEFAULT: '#D4976D', // Muted copper
                    light: '#E5B084',
                    dark: '#B8805A',
                },
                surface: {
                    DEFAULT: '#FFFFFF',
                    dark: '#252526',
                },
                background: {
                    DEFAULT: '#F5F5F5',
                    dark: '#1E1E1E',
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            }
        },
    },
    plugins: [],
    darkMode: 'class', // Enable dark mode via class
}
