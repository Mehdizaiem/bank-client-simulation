"""
Color schemes and theme configuration for the dashboard
"""

COLORS = {
    'primary': '#1e40af',      # Professional blue
    'secondary': '#0f766e',    # Teal
    'accent': '#7c3aed',       # Purple
    'success': '#059669',      # Green
    'warning': '#d97706',      # Orange
    'danger': '#dc2626',       # Red
    'light': '#f8fafc',        # Light gray
    'dark': '#1e293b',         # Dark gray
    'sidebar': '#f1f5f9',      # Sidebar background
    'hover': '#e2e8f0'         # Hover color
}

CHART_COLORS = {
    'line_primary': COLORS['primary'],
    'bar_primary': COLORS['accent'],
    'pie_colors': [COLORS['primary'], COLORS['accent'], COLORS['secondary'], COLORS['success']],
    'map_scale': 'Blues'
}

THEMES = {
    'light': {
        'background': '#ffffff',
        'surface': '#f8fafc',
        'text': '#1e293b',
        'border': '#e2e8f0'
    },
    'dark': {
        'background': '#1e293b',
        'surface': '#334155',
        'text': '#f1f5f9',
        'border': '#475569'
    },
    'corporate': {
        'background': '#f9fafb',
        'surface': '#ffffff',
        'text': '#111827',
        'border': '#d1d5db'
    }
}