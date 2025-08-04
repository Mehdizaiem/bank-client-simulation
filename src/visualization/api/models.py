"""
Data models and schemas for API requests and responses
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ClientSegment(Enum):
    """Client segment enumeration."""
    RETAIL = "retail"
    CORPORATE = "corporate"
    SME = "sme"
    PRIVATE = "private"
    ALL = "all"


class DataExportFormat(Enum):
    """Data export format enumeration."""
    CSV = "csv"
    JSON = "json"
    EXCEL = "xlsx"


@dataclass
class APIResponse:
    """Base API response model."""
    status: str
    timestamp: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@dataclass
class ClientGrowthData:
    """Client growth data model."""
    months: List[str]
    clients: List[int]
    total_clients: int
    growth_rate: Optional[float] = None


@dataclass
class ClientSegmentData:
    """Client segment data model."""
    segment: str
    count: int
    percentage: float


@dataclass
class ClientSegmentationResponse:
    """Client segmentation response model."""
    segments: List[ClientSegmentData]
    total_clients: int


@dataclass
class MonthlyRevenueData:
    """Monthly revenue data model."""
    month: str
    revenue: float
    formatted_revenue: str


@dataclass
class RevenueResponse:
    """Revenue response model."""
    monthly_revenue: List[MonthlyRevenueData]
    total_revenue: float
    average_revenue: float


@dataclass
class GeographicData:
    """Geographic distribution data model."""
    governorate: str
    client_count: int
    percentage: float


@dataclass
class GeographicResponse:
    """Geographic distribution response model."""
    distribution: List[GeographicData]
    total_clients: int


@dataclass
class EconomicIndicatorData:
    """Economic indicator data model."""
    indicator: str
    value: float
    formatted_value: str
    change: Optional[float] = None


@dataclass
class EconomicTrendData:
    """Economic trend data model."""
    month: str
    index: float
    change: float


@dataclass
class ChatMessage:
    """Chat message model."""
    user_message: str
    ai_response: str
    timestamp: str


@dataclass
class ChatRequest:
    """Chat request model."""
    message: str
    context: Optional[Dict[str, Any]] = None


@dataclass
class MetricData:
    """Metric data model."""
    icon: str
    title: str
    value: str
    change: str
    color: Optional[str] = None


@dataclass
class MetricsSummary:
    """Metrics summary model."""
    total_clients: int
    total_revenue: float
    growth_rate: float
    top_segment: str
    last_updated: str


@dataclass
class BranchData:
    """Branch data model."""
    branch_type: str
    count: int
    percentage: float
    location: Optional[str] = None


@dataclass
class ExportRequest:
    """Data export request model."""
    data_type: str
    format: DataExportFormat
    filters: Optional[Dict[str, Any]] = None
    date_range: Optional[Dict[str, str]] = None


@dataclass
class ExportResponse:
    """Data export response model."""
    filename: str
    content: str
    content_type: str
    size: int


@dataclass
class HealthCheckResponse:
    """Health check response model."""
    status: str
    timestamp: str
    version: str
    uptime: Optional[float] = None


@dataclass
class ErrorResponse:
    """Error response model."""
    status: str
    message: str
    timestamp: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# ==================== VALIDATION FUNCTIONS ====================

def validate_client_segment(segment: str) -> bool:
    """Validate client segment value."""
    try:
        ClientSegment(segment)
        return True
    except ValueError:
        return False


def validate_export_format(format_type: str) -> bool:
    """Validate export format value."""
    try:
        DataExportFormat(format_type)
        return True
    except ValueError:
        return False


def validate_date_string(date_str: str) -> bool:
    """Validate date string format (ISO format)."""
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False


# ==================== CONVERSION FUNCTIONS ====================

def dict_to_client_growth_data(data: Dict[str, Any]) -> ClientGrowthData:
    """Convert dictionary to ClientGrowthData."""
    return ClientGrowthData(
        months=data.get('months', []),
        clients=data.get('clients', []),
        total_clients=data.get('total_clients', 0),
        growth_rate=data.get('growth_rate')
    )


def dict_to_revenue_response(data: Dict[str, Any]) -> RevenueResponse:
    """Convert dictionary to RevenueResponse."""
    monthly_data = []
    for item in data.get('monthly_revenue', []):
        monthly_data.append(MonthlyRevenueData(
            month=item.get('month', ''),
            revenue=item.get('revenue', 0.0),
            formatted_revenue=item.get('formatted_revenue', '')
        ))
    
    return RevenueResponse(
        monthly_revenue=monthly_data,
        total_revenue=data.get('total_revenue', 0.0),
        average_revenue=data.get('average_revenue', 0.0)
    )


def dict_to_geographic_response(data: Dict[str, Any]) -> GeographicResponse:
    """Convert dictionary to GeographicResponse."""
    distribution_data = []
    for item in data.get('distribution', []):
        distribution_data.append(GeographicData(
            governorate=item.get('governorate', ''),
            client_count=item.get('client_count', 0),
            percentage=item.get('percentage', 0.0)
        ))
    
    return GeographicResponse(
        distribution=distribution_data,
        total_clients=data.get('total_clients', 0)
    )


# ==================== SCHEMA VALIDATION ====================

def validate_api_response(response_data: Dict[str, Any]) -> bool:
    """Validate API response structure."""
    required_fields = ['status', 'timestamp']
    return all(field in response_data for field in required_fields)


def validate_chat_request(request_data: Dict[str, Any]) -> bool:
    """Validate chat request structure."""
    return 'message' in request_data and isinstance(request_data['message'], str)


def validate_export_request(request_data: Dict[str, Any]) -> bool:
    """Validate export request structure."""
    required_fields = ['data_type', 'format']
    return all(field in request_data for field in required_fields)


# ==================== EXAMPLE SCHEMAS ====================

EXAMPLE_SCHEMAS = {
    'client_growth': {
        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'clients': [11500, 12000, 12250, 12500, 12800, 12847],
        'total_clients': 12847,
        'growth_rate': 11.7
    },
    'chat_request': {
        'message': 'What are the current market trends?',
        'context': {'page': 'economic'}
    },
    'export_request': {
        'data_type': 'clients',
        'format': 'csv',
        'filters': {'segment': 'retail'},
        'date_range': {'start': '2024-01-01', 'end': '2024-06-30'}
    }
}