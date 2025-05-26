
import type { Config } from "tailwindcss";

export default {
	darkMode: ["class"], // Keep dark mode if needed, but we'll force a dark theme via CSS
	content: [
		"./pages/**/*.{ts,tsx}",
		"./components/**/*.{ts,tsx}",
		"./app/**/*.{ts,tsx}",
		"./src/**/*.{ts,tsx}",
	],
	prefix: "",
	theme: {
		container: {
			center: true,
			padding: '2rem',
			screens: {
				'2xl': '1400px'
			}
		},
		extend: {
			fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
			colors: {
        border: 'hsl(var(--border))', // Emerald-tinged border
        input: 'hsl(var(--input))', // Darker input background
        ring: 'hsl(var(--ring))', // Emerald for focus rings
        background: 'hsl(var(--background))', // Matte Black
        foreground: 'hsl(var(--foreground))', // White
        primary: {
          DEFAULT: 'hsl(var(--primary))', // Deep Emerald Green
          foreground: 'hsl(var(--primary-foreground))' // White for text on primary
        },
        secondary: { // A slightly lighter green or dark gray for secondary elements
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))', // Dark gray for muted backgrounds
          foreground: 'hsl(var(--muted-foreground))' // Light gray for muted text
        },
        accent: { // Can be a brighter green or white
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))', // Dark popover background
          foreground: 'hsl(var(--popover-foreground))'
        },
        card: {
          DEFAULT: 'hsl(var(--card))', // Dark card background
          foreground: 'hsl(var(--card-foreground))'
        },
        // Specific sidebar colors can be defined here if needed, or use general theme colors
        sidebar: {
					DEFAULT: 'hsl(var(--sidebar-background))', // Slightly lighter black or dark gray
					foreground: 'hsl(var(--sidebar-foreground))', // White / Light Gray
					primary: 'hsl(var(--primary))', // Emerald for active/hover
					'primary-foreground': 'hsl(var(--primary-foreground))',
					accent: 'hsl(var(--accent))',
					'accent-foreground': 'hsl(var(--accent-foreground))',
					border: 'hsl(var(--border))',
					ring: 'hsl(var(--ring))'
				}
      },
			borderRadius: {
        lg: 'calc(var(--radius) + 4px)', // More rounded
        md: 'var(--radius)',
        sm: 'calc(var(--radius) - 2px)'
      },
			keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' }
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' }
        },
        'fade-in-pop': {
          '0%': { opacity: '0', transform: 'scale(0.9)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        },
        'slide-in-fade': {
          '0%': { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
        },
        'pulse-lite': {
          '0%, 100%': { boxShadow: '0 0 0 0 hsla(var(--primary), 0.4)' },
          '50%': { boxShadow: '0 0 0 5px hsla(var(--primary), 0)' }
        },
        'fade-scale-up': {
          '0%': { opacity: '0', transform: 'scale(0.95) translateY(10px)' },
          '100%': { opacity: '1', transform: 'scale(1) translateY(0)' }
        }
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in-pop': 'fade-in-pop 0.3s ease-out forwards',
        'slide-in-fade': 'slide-in-fade 0.4s ease-out forwards',
        'pulse-lite': 'pulse-lite 1.5s infinite',
        'fade-scale-up': 'fade-scale-up 0.3s ease-out forwards',
      },
      boxShadow: {
        'soft': '0 4px 15px rgba(0, 0, 0, 0.2), 0 2px 8px rgba(0, 0, 0, 0.15)',
        'glow-primary': '0 0 15px 2px hsla(var(--primary-raw), 0.5)',
      }
		}
	},
	plugins: [require("tailwindcss-animate")],
} satisfies Config;
