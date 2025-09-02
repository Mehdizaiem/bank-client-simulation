"""
Color configuration for Bank Client Simulation Platform
"""

# Main color palette
COLORS = {
    'primary': '#1E40AF',      # Blue
    'secondary': '#7C3AED',    # Purple
    'success': '#10B981',      # Green
    'danger': '#EF4444',       # Red
    'warning': '#F59E0B',      # Amber
    'info': '#0EA5E9',         # Sky Blue (used in charts/KPIs)
    'accent': '#8B5CF6',       # Violet
    'dark': '#1F2937',         # Dark Gray
    'light': '#F9FAFB',        # Light Gray
    'hover': '#E5E7EB'         # Hover Gray
}

# Chart color schemes
CHART_COLORS = {
    'primary_gradient': ['#1E40AF', '#3B82F6', '#60A5FA'],
    'success_gradient': ['#10B981', '#34D399', '#6EE7B7'],
    'warning_gradient': ['#F59E0B', '#FBBF24', '#FCD34D'],
    'danger_gradient': ['#EF4444', '#F87171', '#FCA5A5'],
    'multi_color': ['#1E40AF', '#10B981', '#F59E0B', '#EF4444', '#7C3AED', '#8B5CF6'],
    'tunisia_map': ['#EFF6FF', '#DBEAFE', '#BFDBFE', '#93C5FD', '#60A5FA', '#3B82F6', '#2563EB', '#1D4ED8', '#1E40AF']
}

# Status colors
STATUS_COLORS = {
    'online': '#10B981',
    'offline': '#EF4444',
    'warning': '#F59E0B',
    'pending': '#6B7280'
}

# Semantic colors for specific use cases
SEMANTIC_COLORS = {
    'profit': '#10B981',
    'loss': '#EF4444',
    'neutral': '#6B7280',
    'growth': '#10B981',
    'decline': '#EF4444',
    'stable': '#F59E0B'
}
