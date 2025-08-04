"""
Chart controller handling all chart update callbacks
"""
from dash import Input, Output
from services.data_service import DataService
from services.chart_service import ChartService


def register_callbacks(app):
    """Register all chart-related callbacks."""
    
    @app.callback(
        [Output('homepage-line-chart', 'figure'),
         Output('homepage-bar-chart', 'figure'),
         Output('homepage-pie-chart', 'figure'),
         Output('homepage-map-chart', 'figure')],
        Input('current-page-store', 'data'),
        prevent_initial_call=False
    )
    def update_homepage_charts(current_page):
        """Update homepage charts."""
        if current_page != 'home':
            return {}, {}, {}, {}

        # Get data from service
        months, clients = DataService.get_client_growth_data()
        _, revenue = DataService.get_revenue_data()
        segments, sizes = DataService.get_client_segmentation_data()
        governorates, counts = DataService.get_governorate_data()

        # Create charts using service
        line_fig = ChartService.create_client_growth_chart(months, clients)
        bar_fig = ChartService.create_revenue_chart(months, revenue)
        pie_fig = ChartService.create_segmentation_chart(segments, sizes)
        map_fig = ChartService.create_governorate_chart(governorates, counts)

        return line_fig, bar_fig, pie_fig, map_fig
    
    @app.callback(
        [Output('economic-trends-chart', 'figure'), 
         Output('market-indicators-chart', 'figure')],
        Input('current-page-store', 'data'),
        prevent_initial_call=False
    )
    def update_economic_charts(current_page):
        """Update economic analysis charts."""
        if current_page != 'economic':
            return {}, {}
        
        # Get data from service
        months, economic_data = DataService.get_economic_trends()
        indicators, values = DataService.get_economic_indicators()
        
        # Create charts using service
        trends_fig = ChartService.create_economic_trends_chart(months, economic_data)
        indicators_fig = ChartService.create_market_indicators_chart(indicators, values)
        
        return trends_fig, indicators_fig
    
    @app.callback(
        [Output('tunisia-map', 'figure'), 
         Output('branch-distribution-chart', 'figure')],
        Input('current-page-store', 'data'),
        prevent_initial_call=False
    )
    def update_geographic_charts(current_page):
        """Update geographic analysis charts."""
        if current_page != 'geographic':
            return {}, {}
        
        # Get data from service
        governorates, client_counts = DataService.get_governorate_data()
        branch_types, branch_counts = DataService.get_branch_distribution()
        
        # Create charts using service
        map_fig = ChartService.create_governorate_chart(governorates, client_counts)
        branch_fig = ChartService.create_branch_distribution_chart(branch_types, branch_counts)
        
        return map_fig, branch_fig