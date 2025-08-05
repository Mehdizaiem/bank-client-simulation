"""
Configuration settings for Bank Client Simulation Platform
"""

# Dashboard layout configuration
DASHBOARD_CONFIG = {
    'sidebar_width': 280,
    'header_height': 80,
    'chart_height': 300,
    'chat_height': 400,
    'default_padding': 20,
    'card_border_radius': 12,
    'animation_duration': 300
}

# Chat configuration
CHAT_CONFIG = {
    'max_messages': 50,
    'auto_scroll': True,
    'typing_delay': 1000,
    'max_input_length': 500,
    'enable_suggestions': True,
    'enable_quick_actions': True
}

# Simulation configuration
SIMULATION_CONFIG = {
    'default_agent_count': 50000,
    'max_agent_count': 100000,
    'min_agent_count': 1000,
    'update_frequency': 60,  # seconds
    'batch_size': 1000,
    'enable_real_time': True,
    'auto_save_results': True
}

# Economic indicators configuration
ECONOMIC_CONFIG = {
    'default_currency': 'TND',
    'base_interest_rate': 8.0,
    'inflation_threshold': 5.0,
    'gdp_growth_target': 3.0,
    'update_interval': 3600,  # 1 hour in seconds
    'data_retention_days': 365
}

# Geographic configuration
GEOGRAPHIC_CONFIG = {
    'default_governorates': [
        'tunis', 'ariana', 'ben_arous', 'manouba',
        'sfax', 'sousse', 'nabeul', 'bizerte',
        'kairouan', 'gabes', 'medenine', 'monastir'
    ],
    'map_center': {'lat': 34.0, 'lon': 9.0},
    'default_zoom': 6,
    'enable_clustering': True,
    'min_zoom': 5,
    'max_zoom': 12
}

# AI/ML configuration
AI_CONFIG = {
    'default_model': 'ctgan',
    'models_available': ['ctgan', 'tvae', 'gpt4', 'arabic_llm'],
    'max_training_time': 3600,  # 1 hour
    'model_update_frequency': 86400,  # 24 hours
    'enable_continuous_learning': True,
    'memory_retention_days': 90
}

# Data configuration
DATA_CONFIG = {
    'max_file_size_mb': 100,
    'supported_formats': ['csv', 'xlsx', 'json', 'parquet'],
    'backup_frequency': 3600,  # 1 hour
    'compression_enabled': True,
    'encryption_enabled': True,
    'gdpr_compliant': True
}

# Performance configuration
PERFORMANCE_CONFIG = {
    'cache_enabled': True,
    'cache_ttl': 300,  # 5 minutes
    'max_concurrent_users': 100,
    'rate_limit_per_minute': 60,
    'enable_compression': True,
    'optimize_charts': True
}

# Security configuration
SECURITY_CONFIG = {
    'session_timeout': 3600,  # 1 hour
    'max_login_attempts': 3,
    'password_min_length': 8,
    'enable_2fa': True,
    'audit_log_enabled': True,
    'ip_whitelist_enabled': False
}

# Notification configuration
NOTIFICATION_CONFIG = {
    'email_enabled': True,
    'push_enabled': True,
    'slack_enabled': False,
    'alert_thresholds': {
        'high_risk': 0.8,
        'medium_risk': 0.6,
        'low_risk': 0.3
    },
    'batch_notifications': True
}

# Export configuration
EXPORT_CONFIG = {
    'default_format': 'csv',
    'max_export_rows': 100000,
    'include_metadata': True,
    'compress_exports': True,
    'email_large_exports': True,
    'retention_days': 30
}

# API configuration
API_CONFIG = {
    'version': 'v1',
    'base_url': '/api/v1',
    'rate_limit': 1000,  # requests per hour
    'timeout': 30,  # seconds
    'enable_swagger': True,
    'enable_cors': True
}