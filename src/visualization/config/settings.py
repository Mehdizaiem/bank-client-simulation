"""
Application configuration and settings
"""

# Application Settings
APP_CONFIG = {
    'app_name': 'Bank Client Simulation Dashboard',
    'version': '1.0.0',
    'debug': True,
    'host': '0.0.0.0',
    'port': 8050
}

# Dashboard Settings
DASHBOARD_CONFIG = {
    'default_page': 'home',
    'sidebar_width': '280px',
    'chart_height': 320,
    'chat_height': 400,
    'refresh_interval': 15  # seconds
}

# Navigation Menu Items
NAVIGATION_ITEMS = [
    {'icon': '🏠', 'label': 'Home', 'page_id': 'home'},
    {'icon': '📊', 'label': 'Economic Analysis', 'page_id': 'economic'},
    {'icon': '🗺️', 'label': 'Geographic Analysis', 'page_id': 'geographic'},
    {'icon': '💬', 'label': 'AI Chat', 'page_id': 'chat'},
    {'icon': '⚙️', 'label': 'Settings', 'page_id': 'settings'},
]

# Export Settings
EXPORT_CONFIG = {
    'csv_filename': 'dashboard_data.csv',
    'supported_formats': ['CSV', 'PNG', 'PDF']
}

# Chat Settings
CHAT_CONFIG = {
    'ai_name': 'Banking Assistant',
    'ai_icon': '🤖',
    'user_icon': '👤',
    'welcome_message': "Hello! I'm your AI banking assistant. How can I help you analyze client behavior today?"
}