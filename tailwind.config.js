/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/assets/js',
    './apps/*/templates/**/*.html',
    './apps/*/*.py',
  ],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '5rem',
      },
    },
    extend: {
      colors: {
        'alert-success': 'hsl(var(--alert-success) / <alpha-value>)',
        'alert-error': 'hsl(var(--alert-error) / <alpha-value>)',
        'alert-warning': 'hsl(var(--alert-warning) / <alpha-value>)',
        'alert-info': 'hsl(var(--alert-info) / <alpha-value>)',
        'alert-secondary': 'hsl(var(--alert-secondary) / <alpha-value>)',
      }
    },
    },
  plugins: [],
}