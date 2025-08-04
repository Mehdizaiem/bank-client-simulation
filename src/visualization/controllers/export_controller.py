"""
Export controller handling data export functionality
"""
from dash import Input, Output, dcc
from services.data_service import DataService


def register_callbacks(app):
    """Register all export-related callbacks."""
    
    @app.callback(
        Output("home-csv-download", "data"),
        Input("home-export-csv", "n_clicks"),
        prevent_initial_call=True
    )
    def download_homepage_csv(n_clicks):
        """Download homepage data as CSV."""
        df = DataService.generate_export_data()
        return dcc.send_data_frame(df.to_csv, "dashboard_data.csv")
    
    # Add more export callbacks as needed for other pages
    # Example for economic data export:
    
    # @app.callback(
    #     Output("economic-csv-download", "data"),
    #     Input("economic-export-btn", "n_clicks"),
    #     prevent_initial_call=True
    # )
    # def download_economic_csv(n_clicks):
    #     """Download economic data as CSV."""
    #     # Generate economic-specific data
    #     df = DataService.generate_economic_export_data()
    #     return dcc.send_data_frame(df.to_csv, "economic_analysis.csv")