/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                obsidian: {
                    base: '#0b0c10',
                    surface: '#1f2833',
                    overlay: 'rgba(11, 12, 16, 0.7)',
                },
                neon: {
                    cyan: '#66fcf1',
                    purple: '#c5a3ff',
                },
                chrome: {
                    border: 'rgba(255, 255, 255, 0.15)',
                    highlight: 'rgba(255, 255, 255, 0.25)',
                }
            },
            fontFamily: {
                heading: ['Saira', 'sans-serif'],
                body: ['Outfit', 'sans-serif'],
            },
            backgroundImage: {
                'void-grid': "linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
                'liquid-metal': "linear-gradient(135deg, #1f2833 0%, #0b0c10 100%)",
            },
            boxShadow: {
                'neon-glow': '0 0 15px rgba(102, 252, 241, 0.15)',
                'neon-strong': '0 0 30px rgba(102, 252, 241, 0.4)',
            }
        },
    },
    plugins: [],
}
