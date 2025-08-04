"""
Utility functions and helpers
"""
import pandas as pd
from typing import Any, Dict, List


def format_currency(amount: float, currency: str = "€") -> str:
    """Format amount as currency."""
    if amount >= 1_000_000:
        return f"{currency}{amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{currency}{amount/1_000:.1f}K"
    else:
        return f"{currency}{amount:.2f}"


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format value as percentage."""
    return f"{value:.{decimal_places}f}%"


def format_number(value: int) -> str:
    """Format number with thousands separator."""
    return f"{value:,}"


def validate_data(data: Any) -> bool:
    """Validate data is not None or empty."""
    if data is None:
        return False
    if isinstance(data, (list, dict, str)) and len(data) == 0:
        return False
    return True


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, return default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values."""
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters."""
    import re
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def convert_to_dataframe(data: List[Dict]) -> pd.DataFrame:
    """Convert list of dictionaries to pandas DataFrame."""
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


def get_color_by_value(value: float, thresholds: Dict[str, float], colors: Dict[str, str]) -> str:
    """Get color based on value thresholds."""
    if value >= thresholds.get('high', 80):
        return colors.get('success', '#059669')
    elif value >= thresholds.get('medium', 50):
        return colors.get('warning', '#d97706')
    else:
        return colors.get('danger', '#dc2626')


def generate_gradient_colors(start_color: str, end_color: str, steps: int) -> List[str]:
    """Generate gradient colors between two colors."""
    # This is a simplified implementation - you might want to use a proper color library
    return [start_color] * steps  # Placeholder implementation