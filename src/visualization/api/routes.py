"""
REST API routes for the Bank Dashboard application
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
from services.data_service import DataService
from services.ai_service import AIService
from utils.helpers import format_currency, format_percentage


# Create Flask app for API endpoints
api_app = Flask(__name__)
CORS(api_app)  # Enable CORS for cross-origin requests


# ==================== DATA ENDPOINTS ====================

@api_app.route('/api/clients/growth', methods=['GET'])
def get_client_growth():
    """Get client growth data over time."""
    try:
        months, clients = DataService.get_client_growth_data()
        return jsonify({
            'status': 'success',
            'data': {
                'months': months,
                'clients': clients,
                'total_clients': clients[-1] if clients else 0
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_app.route('/api/clients/segmentation', methods=['GET'])
def get_client_segmentation():
    """Get client segmentation data."""
    try:
        segments, sizes = DataService.get_client_segmentation_data()
        total = sum(sizes)
        
        segmentation_data = []
        for segment, size in zip(segments, sizes):
            segmentation_data.append({
                'segment': segment,
                'count': size,
                'percentage': round((size / total) * 100, 2) if total > 0 else 0
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'segments': segmentation_data,
                'total_clients': total
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_app.route('/api/revenue/monthly', methods=['GET'])
def get_monthly_revenue():
    """Get monthly revenue data."""
    try:
        months, revenue = DataService.get_revenue_data()
        
        revenue_data = []
        for month, rev in zip(months, revenue):
            revenue_data.append({
                'month': month,
                'revenue': rev,
                'formatted_revenue': format_currency(rev * 1000)  # Convert from K to actual amount
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'monthly_revenue': revenue_data,
                'total_revenue': sum(revenue),
                'average_revenue': round(sum(revenue) / len(revenue), 2) if revenue else 0
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_app.route('/api/geography/distribution', methods=['GET'])
def get_geographic_distribution():
    """Get geographic distribution data."""
    try:
        governorates, counts = DataService.get_governorate_data()
        
        geo_data = []
        total_clients = sum(counts)
        
        for gov, count in zip(governorates, counts):
            geo_data.append({
                'governorate': gov,
                'client_count': count,
                'percentage': round((count / total_clients) * 100, 2) if total_clients > 0 else 0
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'distribution': geo_data,
                'total_clients': total_clients
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== ECONOMIC ENDPOINTS ====================

@api_app.route('/api/economic/indicators', methods=['GET'])
def get_economic_indicators():
    """Get economic indicators data."""
    try:
        indicators, values = DataService.get_economic_indicators()
        
        indicator_data = []
        for indicator, value in zip(indicators, values):
            indicator_data.append({
                'indicator': indicator,
                'value': round(value, 2),
                'formatted_value': format_percentage(value) if 'rate' in indicator.lower() else f"{value:.2f}"
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'indicators': indicator_data
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_app.route('/api/economic/trends', methods=['GET'])
def get_economic_trends():
    """Get economic trends over time."""
    try:
        months, trends = DataService.get_economic_trends()
        
        trend_data = []
        for month, trend in zip(months, trends):
            trend_data.append({
                'month': month,
                'index': trend,
                'change': round(trend - 100, 2)  # Change from baseline of 100
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'trends': trend_data,
                'current_index': trends[-1] if trends else 100
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== AI CHAT ENDPOINTS ====================

@api_app.route('/api/chat/message', methods=['POST'])
def process_chat_message():
    """Process AI chat message."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message.strip():
            return jsonify({
                'status': 'error',
                'message': 'Message cannot be empty'
            }), 400
        
        ai_response = AIService.process_user_message(user_message)
        
        return jsonify({
            'status': 'success',
            'data': {
                'user_message': user_message,
                'ai_response': ai_response,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_app.route('/api/chat/suggestions', methods=['GET'])
def get_chat_suggestions():
    """Get suggested chat questions."""
    try:
        suggestions = AIService.get_suggested_questions()
        
        return jsonify({
            'status': 'success',
            'data': {
                'suggestions': suggestions
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== METRICS ENDPOINTS ====================

@api_app.route('/api/metrics/key', methods=['GET'])
def get_key_metrics():
    """Get key dashboard metrics."""
    try:
        metrics = DataService.get_key_metrics()
        
        return jsonify({
            'status': 'success',
            'data': {
                'metrics': metrics
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_app.route('/api/metrics/summary', methods=['GET'])
def get_metrics_summary():
    """Get comprehensive metrics summary."""
    try:
        # Compile data from multiple sources
        months, clients = DataService.get_client_growth_data()
        _, revenue = DataService.get_revenue_data()
        segments, sizes = DataService.get_client_segmentation_data()
        
        summary = {
            'total_clients': clients[-1] if clients else 0,
            'total_revenue': sum(revenue) if revenue else 0,
            'growth_rate': round(((clients[-1] - clients[0]) / clients[0]) * 100, 2) if len(clients) > 1 and clients[0] != 0 else 0,
            'top_segment': segments[sizes.index(max(sizes))] if segments and sizes else 'N/A',
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'data': summary
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== EXPORT ENDPOINTS ====================

@api_app.route('/api/export/csv/<data_type>', methods=['GET'])
def export_csv_data(data_type):
    """Export data as CSV."""
    try:
        if data_type == 'clients':
            df = DataService.generate_export_data()
            csv_data = df.to_csv(index=False)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid data type'}), 400
        
        return jsonify({
            'status': 'success',
            'data': {
                'csv_content': csv_data,
                'filename': f'{data_type}_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== HEALTH CHECK ENDPOINT ====================

@api_app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


# ==================== ERROR HANDLERS ====================

@api_app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404


@api_app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500


if __name__ == '__main__':
    api_app.run(debug=True, host='0.0.0.0', port=5000)