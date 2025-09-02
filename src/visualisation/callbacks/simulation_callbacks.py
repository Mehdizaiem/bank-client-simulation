"""
Corrected Simulation Callbacks - Complete File
Replace callbacks/simulation_callbacks.py with this version
"""
import os
import json
import subprocess
import plotly.graph_objects as go
from pathlib import Path
from dash import Input, Output, State, html, dcc, no_update, ctx
from dash.exceptions import PreventUpdate
from config.colors import COLORS
import io
from datetime import datetime

def register_simulation_callbacks(app):
    """Register simulation-related callbacks"""
    
    @app.callback(
        [Output('simulation-status-display', 'children'),
         Output('data-refresh-token', 'data'),
         Output('run-simulation-btn', 'disabled'),
         Output('run-simulation-btn', 'children'),
         Output('simulation-results-container', 'children')],
        [Input('run-simulation-btn', 'n_clicks'),
         Input('load-results-btn', 'n_clicks'),
         Input('reset-simulation-btn', 'n_clicks')],
        [State('agent-count-input', 'value'),
         State('retail-ratio-slider', 'value'),
         State('time-steps-input', 'value'),
         State('seed-input', 'value'),
         State('scenario-selector', 'value'),
         State('data-refresh-token', 'data')]
    )
    def handle_simulation_controls(run_clicks, load_clicks, reset_clicks, 
                                 num_agents, retail_ratio, time_steps, seed, scenario, refresh_token):
        """Handle all simulation control buttons"""
        
        # Determine which input fired
        if ctx.triggered:
            trigger_id = ctx.triggered_id
        else:
            return (no_update, no_update, False,
                    [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"],
                    no_update)
        
        # Reset button
        if trigger_id == 'reset-simulation-btn' and reset_clicks:
            return (
                create_status_message("Ready to run simulation", "info"),
                refresh_token + 1,
                False,
                [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"],
                []
            )
        
        # Load latest results
        if trigger_id == 'load-results-btn' and load_clicks:
            return load_simulation_results(refresh_token)
        
        # Run simulation
        if trigger_id == 'run-simulation-btn' and run_clicks:
            return run_simulation(num_agents, retail_ratio, time_steps, seed, scenario, refresh_token)
        
        return no_update, no_update, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], no_update
    @app.callback(
        Output('download-pdf', 'data'),
        Output('download-excel', 'data'),
        Output('download-json', 'data'),
        Output('export-status', 'children', allow_duplicate=True),
        Input('export-pdf-btn', 'n_clicks'),
        Input('export-excel-btn', 'n_clicks'),
        Input('export-json-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def handle_exports(pdf_clicks, excel_clicks, json_clicks):
        if not ctx.triggered_id:
            raise PreventUpdate

        # defaults
        pdf_data = no_update
        excel_data = no_update
        json_data = no_update
        status = no_update

        output_dir = Path('output/dashboard_exports')
        bundle_path = output_dir / 'dashboard_bundle_enhanced.json'

        # ---------- JSON ----------
        if ctx.triggered_id == 'export-json-btn':
            if not bundle_path.exists():
                status = html.Div("⚠️ No simulation results found. Run a simulation first.",
                                style={'color': '#f59e0b', 'textAlign': 'center', 'fontSize': '0.9rem'})
            else:
                text = bundle_path.read_text(encoding='utf-8')
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                json_data = dcc.send_string(text, f"simulation_results_{ts}.json")
                status = html.Div("✅ JSON results generated successfully!",
                                style={'color': '#10b981', 'textAlign': 'center', 'fontSize': '0.9rem'})

        # ---------- Excel ----------
        elif ctx.triggered_id == 'export-excel-btn':
            csv_path = output_dir / 'agents_data_enhanced.csv'
            if not csv_path.exists():
                status = html.Div("⚠️ No simulation data found. Run a simulation first.",
                                style={'color': '#f59e0b', 'textAlign': 'center', 'fontSize': '0.9rem'})
            else:
                try:
                    import pandas as pd
                    buf = io.BytesIO()
                    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                        # Agent data
                        pd.read_csv(csv_path).to_excel(writer, sheet_name='Agent_Data', index=False)
                        # Summary + time series if available
                        if bundle_path.exists():
                            results = json.loads(bundle_path.read_text(encoding='utf-8'))
                            k = results['quick_stats']['headline_numbers']
                            pd.DataFrame([
                                ['Total Clients', k['total_clients']],
                                ['Active Clients', k['active_clients']],
                                ['Satisfaction Score', f"{k['satisfaction_score']:.1f}%"],
                                ['Digital Adoption', f"{k['digital_adoption']:.1f}%"],
                                ['Retention Rate', f"{k['retention_rate']:.1f}%"],
                            ], columns=['Metric', 'Value']).to_excel(writer, sheet_name='Summary', index=False)

                            core = results['simulation_metrics']['time_series']['metrics']['core_metrics']
                            ts = results['simulation_metrics']['time_series']['timestamps']
                            if core and ts:
                                pd.DataFrame({
                                    'Step': [t['step'] for t in ts],
                                    'Satisfaction': core.get('satisfaction', []),
                                    'Churn_Rate': core.get('churn_rate', []),
                                    'Digital_Adoption': core.get('digital_adoption', []),
                                    'Retention_Rate': core.get('retention_rate', []),
                                }).to_excel(writer, sheet_name='Time_Series', index=False)

                    buf.seek(0)
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    excel_data = dcc.send_bytes(buf.getvalue(), f"simulation_data_{ts}.xlsx")
                    status = html.Div("✅ Excel file generated successfully!",
                                    style={'color': '#10b981', 'textAlign': 'center', 'fontSize': '0.9rem'})
                except Exception as e:
                    status = html.Div(f"❌ Excel export failed: {e}",
                                    style={'color': '#ef4444', 'textAlign': 'center', 'fontSize': '0.9rem'})

        # ---------- PDF ----------
        elif ctx.triggered_id == 'export-pdf-btn':
            if not bundle_path.exists():
                status = html.Div("⚠️ No simulation results found. Run a simulation first.",
                                style={'color': '#f59e0b', 'textAlign': 'center', 'fontSize': '0.9rem'})
            else:
                try:
                    from reportlab.lib.pagesizes import A4
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.lib import colors

                    results = json.loads(bundle_path.read_text(encoding='utf-8'))
                    k = results['quick_stats']['headline_numbers']
                    buf = io.BytesIO()
                    doc = SimpleDocTemplate(buf, pagesize=A4)
                    styles = getSampleStyleSheet()
                    story = []

                    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.darkblue)
                    story.append(Paragraph("Bank Client Simulation Report", title_style))
                    story.append(Spacer(1, 20))

                    data = [
                        ['Metric', 'Value'],
                        ['Total Clients', f"{k['total_clients']:,}"],
                        ['Satisfaction Score', f"{k['satisfaction_score']:.1f}%"],
                        ['Digital Adoption', f"{k['digital_adoption']:.1f}%"],
                        ['Retention Rate', f"{k['retention_rate']:.1f}%"],
                    ]
                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ]))
                    story.append(Paragraph("Simulation Summary", styles['Heading2']))
                    story.append(table)
                    story.append(Spacer(1, 20))

                    # Config (guard % formatting)
                    cfg = results.get('simulation_metrics', {}).get('metadata', {}).get('config', {})
                    rr = cfg.get('retail_ratio')
                    rr_text = f"{rr:.1%}" if isinstance(rr, (int, float)) else str(rr)
                    cfg_html = (
                        f"Number of Agents: {cfg.get('num_agents','N/A')}<br/>"
                        f"Retail Ratio: {rr_text}<br/>"
                        f"Time Steps: {cfg.get('time_steps','N/A')}<br/>"
                        f"Random Seed: {cfg.get('random_seed','N/A')}<br/>"
                        f"Scenario: {str(cfg.get('scenario','N/A')).title()}"
                    )
                    story.append(Paragraph("Configuration Used", styles['Heading2']))
                    story.append(Paragraph(cfg_html, styles['Normal']))
                    story.append(Spacer(1, 20))

                    story.append(Paragraph(datetime.now().strftime("Generated: %Y-%m-%d %H:%M:%S"), styles['Normal']))
                    doc.build(story)
                    buf.seek(0)

                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    pdf_data = dcc.send_bytes(buf.getvalue(), f"simulation_report_{ts}.pdf")
                    status = html.Div("✅ PDF report generated successfully!",
                                    style={'color': '#10b981', 'textAlign': 'center', 'fontSize': '0.9rem'})
                except ImportError as e:
                    status = html.Div(f"⚠️ PDF export requires reportlab. {e}",
                                    style={'color': '#f59e0b', 'textAlign': 'center', 'fontSize': '0.9rem'})
                except Exception as e:
                    status = html.Div(f"❌ PDF export failed: {e}",
                                    style={'color': '#ef4444', 'textAlign': 'center', 'fontSize': '0.9rem'})

        return pdf_data, excel_data, json_data, status
def create_status_message(message, status_type="info"):
    """Create a status message with appropriate styling"""
    color_map = {
        "info": "#3b82f6",
        "success": "#10b981", 
        "warning": "#f59e0b",
        "error": "#ef4444",
        "running": "#8b5cf6"
    }
    
    bg_color_map = {
        "info": "#dbeafe",
        "success": "#d1fae5",
        "warning": "#fef3c7", 
        "error": "#fee2e2",
        "running": "#f3e8ff"
    }
    
    icon_map = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️", 
        "error": "❌",
        "running": "⏳"
    }
    
    return html.Div([
        html.Span(icon_map.get(status_type, "ℹ️"), style={'marginRight': '8px', 'fontSize': '16px'}),
        message
    ], style={
        'padding': '15px',
        'backgroundColor': bg_color_map.get(status_type, "#dbeafe"),
        'color': color_map.get(status_type, "#3b82f6"),
        'borderRadius': '8px',
        'fontWeight': '500',
        'textAlign': 'center',
        'marginBottom': '15px'
    })

def run_simulation(num_agents, retail_ratio, time_steps, seed, scenario, refresh_token):
    """Run the simulation by executing test_simulation_direct.py with dashboard parameters"""
    try:
        # Create status message for running
        status_msg = create_status_message(
            f"Running simulation with {num_agents} agents, {time_steps} steps, scenario: {scenario}...", 
            "running"
        )
        
        # Try different approaches to find and execute the script
        script_paths = [
            Path('test_simulation_direct.py'),
            Path('../../test_simulation_direct.py'),
            Path('../../../test_simulation_direct.py'),
        ]
        
        simulation_script = None
        for script_path in script_paths:
            if script_path.exists():
                simulation_script = script_path
                break
        
        if not simulation_script:
            error_msg = create_status_message(
                "Could not find test_simulation_direct.py. Please ensure it's in the project root.", 
                "error"
            )
            return error_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []
        
        # Determine working directory
        if simulation_script.name == 'test_simulation_direct.py' and simulation_script.exists():
            working_dir = Path.cwd()
        else:
            working_dir = simulation_script.parent
        
        print(f"Executing simulation script: {simulation_script.absolute()}")
        print(f"Working directory: {working_dir.absolute()}")
        
        # Prepare environment with UTF-8 encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSSTDIO'] = '1'
        
        # Execute with dashboard parameters
        cmd = [
            'python', simulation_script.name,
            '--num_agents', str(num_agents),
            '--retail_ratio', str(retail_ratio),
            '--time_steps', str(time_steps),
            '--random_seed', str(seed),
            '--scenario', scenario
        ]
        
        print(f"Executing command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(working_dir),
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("Simulation completed successfully")
            print("STDOUT:", result.stdout[-500:] if result.stdout else "No output")
            
            # Store requested parameters for comparison
            requested_params = {
                'requested_agents': num_agents,
                'requested_steps': time_steps,
                'requested_retail_ratio': retail_ratio,
                'requested_seed': seed,
                'requested_scenario': scenario
            }
            
            return load_simulation_results(refresh_token + 1, success_message=True, requested_params=requested_params)
        else:
            print("Simulation failed")
            print("STDERR:", result.stderr if result.stderr else "No error output")
            error_msg = create_status_message(
                f"Simulation failed. Error: {result.stderr[:200] if result.stderr else 'Unknown error'}", 
                "error"
            )
            return error_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []
            
    except subprocess.TimeoutExpired:
        error_msg = create_status_message("Simulation timed out after 5 minutes", "error")
        return error_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []
    except FileNotFoundError as e:
        error_msg = create_status_message(f"Python executable not found: {str(e)}", "error")
        return error_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []
    except Exception as e:
        error_msg = create_status_message(f"Unexpected error: {str(e)}", "error")
        return error_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []

def load_simulation_results(refresh_token, success_message=False, requested_params=None):
    """Load and display simulation results from output folder"""
    try:
        # Check for results files
        output_dir = Path('output/dashboard_exports')
        if not output_dir.exists():
            status_msg = create_status_message("No simulation results found. Please run a simulation first.", "warning")
            return status_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []
        
        # Load the main results bundle
        bundle_path = output_dir / 'dashboard_bundle_enhanced.json'
        if not bundle_path.exists():
            status_msg = create_status_message("Results bundle not found. Please run a simulation first.", "warning")
            return status_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []
        
        with open(bundle_path, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Create success status message
        if success_message:
            status_msg = create_status_message("Simulation completed successfully! Results loaded.", "success")
        else:
            status_msg = create_status_message("Latest simulation results loaded successfully.", "success")
        
        # Create results display
        if requested_params:
            results_display = create_simulation_results_display(results, requested_params)
        else:
            results_display = create_simulation_results_display(results)
        
        return (
            status_msg,
            refresh_token + 1,
            False,
            [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"],
            results_display
        )
        
    except Exception as e:
        error_msg = create_status_message(f"Error loading results: {str(e)}", "error")
        return error_msg, refresh_token, False, [html.Span("🚀 ", style={'fontSize': '18px'}), "Run Simulation"], []

def create_simulation_results_display(results, requested_params=None):
    """Create the simulation results display section"""
    
    # Extract key metrics
    sim_metrics = results.get('simulation_metrics', {})
    final_kpis = sim_metrics.get('kpis', {}).get('final_metrics', {})
    time_series = sim_metrics.get('time_series', {})
    alerts = sim_metrics.get('alerts', [])
    
    # Add parameter comparison section if we have requested parameters
    param_comparison = None
    if requested_params:
        param_comparison = create_parameter_comparison_section(results, requested_params)
    
    return html.Div([
        html.H2("📊 Simulation Results", style={
            'fontSize': '1.8rem',
            'fontWeight': '600', 
            'color': COLORS['dark'],
            'marginBottom': '25px'
        }),
        
        # Parameter Comparison Section
        param_comparison if param_comparison else html.Div(),
        
        # Alert Section
        create_alerts_section(alerts),
        
        # KPI Results Cards
        create_kpi_results_section(final_kpis),
        
        # Time Series Chart
        create_time_series_chart(time_series),
        
        # Export Section
        create_export_section()
    ])

def create_parameter_comparison_section(results, requested_params):
    """Create a section showing requested vs actual parameters"""
    
    # Extract actual parameters from results
    sim_config = results.get('simulation_metrics', {}).get('metadata', {}).get('config', {})
    actual_agents = sim_config.get('num_agents', 'Unknown')
    actual_steps = sim_config.get('time_steps', 'Unknown')
    actual_retail_ratio = sim_config.get('retail_ratio', 'Unknown')
    actual_seed = sim_config.get('random_seed', 'Unknown')
    actual_scenario = sim_config.get('scenario', 'Unknown')
    
    # Compare requested vs actual
    comparisons = [
        {
            'parameter': 'Number of Agents',
            'requested': f"{requested_params['requested_agents']:,}",
            'actual': f"{actual_agents:,}" if actual_agents != 'Unknown' else actual_agents,
            'match': requested_params['requested_agents'] == actual_agents
        },
        {
            'parameter': 'Time Steps',
            'requested': f"{requested_params['requested_steps']:,}",
            'actual': f"{actual_steps:,}" if actual_steps != 'Unknown' else actual_steps,
            'match': requested_params['requested_steps'] == actual_steps
        },
        {
            'parameter': 'Retail Ratio',
            'requested': f"{requested_params['requested_retail_ratio']:.1%}",
            'actual': f"{actual_retail_ratio:.1%}" if actual_retail_ratio != 'Unknown' else actual_retail_ratio,
            'match': abs(requested_params['requested_retail_ratio'] - actual_retail_ratio) < 0.01 if actual_retail_ratio != 'Unknown' else False
        },
        {
            'parameter': 'Random Seed',
            'requested': str(requested_params['requested_seed']),
            'actual': str(actual_seed),
            'match': requested_params['requested_seed'] == actual_seed
        },
        {
            'parameter': 'Scenario',
            'requested': requested_params['requested_scenario'].title(),
            'actual': actual_scenario.title() if actual_scenario != 'Unknown' else actual_scenario,
            'match': requested_params['requested_scenario'] == actual_scenario
        }
    ]
    
    # Create comparison table
    comparison_rows = []
    for comp in comparisons:
        status_icon = "✅" if comp['match'] else "⚠️"
        status_color = COLORS['success'] if comp['match'] else COLORS['warning']
        
        comparison_rows.append(
            html.Tr([
                html.Td(comp['parameter'], style={'fontWeight': '600', 'padding': '8px'}),
                html.Td(comp['requested'], style={'padding': '8px', 'textAlign': 'center'}),
                html.Td(comp['actual'], style={'padding': '8px', 'textAlign': 'center'}),
                html.Td([
                    html.Span(status_icon, style={'marginRight': '5px'}),
                    "Match" if comp['match'] else "Different"
                ], style={'padding': '8px', 'textAlign': 'center', 'color': status_color, 'fontWeight': '500'})
            ])
        )
    
    return html.Div([
        html.H3("⚙️ Parameter Comparison", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'marginBottom': '15px'
        }),
        html.P("Comparison between requested parameters and actual simulation execution:", style={
            'fontSize': '0.9rem',
            'color': COLORS['secondary'],
            'marginBottom': '15px'
        }),
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Parameter", style={'padding': '10px', 'fontWeight': '700'}),
                    html.Th("Requested", style={'padding': '10px', 'textAlign': 'center', 'fontWeight': '700'}),
                    html.Th("Actual", style={'padding': '10px', 'textAlign': 'center', 'fontWeight': '700'}),
                    html.Th("Status", style={'padding': '10px', 'textAlign': 'center', 'fontWeight': '700'})
                ])
            ]),
            html.Tbody(comparison_rows)
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'backgroundColor': 'white',
            'border': '1px solid #e2e8f0'
        }),
        html.Div([
            html.P("✅ Note: The simulation script now accepts dashboard parameters. "
                   "All requested parameters should match the actual execution values.", 
                   style={
                       'fontSize': '0.85rem',
                       'color': COLORS['success'],
                       'fontStyle': 'italic',
                       'marginTop': '10px',
                       'padding': '10px',
                       'backgroundColor': '#d1fae5',
                       'borderRadius': '6px',
                       'border': '1px solid #10b981'
                   })
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
        'marginBottom': '25px'
    })

def create_alerts_section(alerts):
    """Create alerts section if there are any alerts"""
    if not alerts:
        return html.Div()
    
    alert_items = []
    for alert in alerts:
        severity = alert.get('severity', 'medium')
        bg_color = '#fee2e2' if severity == 'high' else '#fef3c7'
        border_color = '#fca5a5' if severity == 'high' else '#fcd34d'
        
        alert_items.append(
            html.Div([
                html.Strong("⚠️ Alert: "),
                alert.get('message', 'Unknown alert')
            ], style={
                'padding': '15px',
                'backgroundColor': bg_color,
                'border': f'1px solid {border_color}',
                'borderRadius': '8px',
                'marginBottom': '10px'
            })
        )
    
    return html.Div([
        html.H3("🚨 Simulation Alerts", style={
            'fontSize': '1.2rem',
            'fontWeight': '600',
            'marginBottom': '15px'
        }),
        html.Div(alert_items, style={'marginBottom': '25px'})
    ])

def create_kpi_results_section(final_kpis):
    """Create KPI results cards section"""
    
    # Calculate derived metrics
    total_agents = final_kpis.get('total_agents', 1000)
    satisfaction = final_kpis.get('final_satisfaction', 0) * 100
    churn_rate = final_kpis.get('final_churn_rate', 0) * 100
    retention_rate = final_kpis.get('final_retention_rate', 0)
    digital_adoption = final_kpis.get('final_digital_adoption', 0) * 100
    
    kpi_cards = [
        create_result_kpi_card(
            "👥", "Total Agents", f"{total_agents:,}", 
            "Simulated", COLORS['primary']
        ),
        create_result_kpi_card(
            "😊", "Final Satisfaction", f"{satisfaction:.1f}%",
            "Excellent" if satisfaction > 65 else "Good" if satisfaction > 55 else "Needs Improvement",
            COLORS['success'] if satisfaction > 65 else COLORS['warning'] if satisfaction > 55 else '#ef4444'
        ),
        create_result_kpi_card(
            "📉", "Churn Rate", f"{churn_rate:.2f}%",
            "Excellent" if churn_rate < 2 else "Good" if churn_rate < 5 else "High Risk",
            COLORS['success'] if churn_rate < 2 else COLORS['warning'] if churn_rate < 5 else '#ef4444'
        ),
        create_result_kpi_card(
            "🔄", "Retention Rate", f"{retention_rate:.1f}%",
            "Outstanding" if retention_rate > 98 else "Excellent" if retention_rate > 95 else "Good",
            COLORS['success'] if retention_rate > 95 else COLORS['warning']
        ),
        create_result_kpi_card(
            "📱", "Digital Adoption", f"{digital_adoption:.1f}%",
            "High" if digital_adoption > 60 else "Medium" if digital_adoption > 40 else "Low",
            COLORS['success'] if digital_adoption > 60 else COLORS['warning'] if digital_adoption > 40 else COLORS['secondary']
        )
    ]
    
    return html.Div([
        html.H3("📈 Key Performance Indicators", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'marginBottom': '20px'
        }),
        html.Div(kpi_cards, style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
            'gap': '20px',
            'marginBottom': '30px'
        })
    ])

def create_result_kpi_card(icon, title, value, change, color):
    """Create a KPI result card"""
    return html.Div([
        html.Div(icon, style={'fontSize': '2rem', 'marginBottom': '8px'}),
        html.Div(value, style={
            'fontSize': '1.8rem',
            'fontWeight': '700',
            'color': color,
            'marginBottom': '4px'
        }),
        html.Div(title, style={
            'fontSize': '0.9rem',
            'color': COLORS['secondary'],
            'fontWeight': '500'
        }),
        html.Div(change, style={
            'fontSize': '0.8rem',
            'color': COLORS['secondary'],
            'marginTop': '4px'
        })
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
        'textAlign': 'center',
        'border': f'2px solid {color}15'
    })

def create_time_series_chart(time_series_data):
    """Create time series evolution chart"""
    if not time_series_data or 'metrics' not in time_series_data:
        return html.Div()
    
    metrics = time_series_data['metrics']['core_metrics']
    timestamps = time_series_data.get('timestamps', [])
    
    # Prepare data for chart
    steps = [ts.get('step', i) for i, ts in enumerate(timestamps)]
    
    # Create the chart
    fig = go.Figure()
    
    # Satisfaction line
    if 'satisfaction' in metrics:
        satisfaction_values = [v * 100 for v in metrics['satisfaction']]
        fig.add_trace(go.Scatter(
            x=steps,
            y=satisfaction_values,
            mode='lines+markers',
            name='Satisfaction (%)',
            line=dict(color=COLORS['success'], width=3),
            yaxis='y'
        ))
    
    # Digital adoption line
    if 'digital_adoption' in metrics:
        digital_values = [v * 100 for v in metrics['digital_adoption']]
        fig.add_trace(go.Scatter(
            x=steps,
            y=digital_values,
            mode='lines+markers', 
            name='Digital Adoption (%)',
            line=dict(color=COLORS['primary'], width=3),
            yaxis='y'
        ))
    
    # Churn rate line (on secondary y-axis)
    if 'churn_rate' in metrics:
        churn_values = [v * 100 for v in metrics['churn_rate']]
        fig.add_trace(go.Scatter(
            x=steps,
            y=churn_values,
            mode='lines+markers',
            name='Churn Rate (%)',
            line=dict(color='#ef4444', width=3),
            yaxis='y2'
        ))
    
    # Update layout
    fig.update_layout(
        title="Simulation Evolution Over Time",
        xaxis_title="Time Step",
        yaxis=dict(title="Satisfaction & Digital Adoption (%)", side="left"),
        yaxis2=dict(title="Churn Rate (%)", side="right", overlaying="y"),
        height=400,
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.8)')
    )
    
    return html.Div([
        html.H3("📈 Simulation Evolution", style={
            'fontSize': '1.3rem',
            'fontWeight': '600',
            'marginBottom': '20px'
        }),
        html.Div([
            dcc.Graph(figure=fig, config={'displayModeBar': False})
        ], style={
            'backgroundColor': 'white',
            'padding': '25px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
            'marginBottom': '25px'
        })
    ])

def create_export_section():
    """Create export options section with download components"""
    return html.Div([
        html.H4("💾 Export Results", style={
            'fontSize': '1.1rem',
            'fontWeight': '600',
            'marginBottom': '15px',
            'textAlign': 'center'
        }),
        html.Div([
            html.Button("📄 Export PDF Report", 
                       id="export-pdf-btn", 
                       n_clicks=0,
                       style={
                           'padding': '10px 20px',
                           'backgroundColor': COLORS['primary'],
                           'color': 'white',
                           'border': 'none',
                           'borderRadius': '6px',
                           'cursor': 'pointer',
                           'marginRight': '10px'
                       }),
            html.Button("📊 Export Excel Data", 
                       id="export-excel-btn",
                       n_clicks=0,
                       style={
                           'padding': '10px 20px',
                           'backgroundColor': COLORS['success'],
                           'color': 'white',
                           'border': 'none',
                           'borderRadius': '6px',
                           'cursor': 'pointer',
                           'marginRight': '10px'
                       }),
            html.Button("💾 Save JSON Results", 
                       id="export-json-btn",
                       n_clicks=0,
                       style={
                           'padding': '10px 20px',
                           'backgroundColor': COLORS['secondary'],
                           'color': 'white',
                           'border': 'none',
                           'borderRadius': '6px',
                           'cursor': 'pointer'
                       })
        ], style={'textAlign': 'center', 'marginBottom': '15px'}),
        
        # Download components (hidden)
        dcc.Download(id="download-pdf"),
        dcc.Download(id="download-excel"), 
        dcc.Download(id="download-json"),
        
        # Status message for export operations
        html.Div(id="export-status", style={'marginTop': '10px'}),
        
        html.P("Files will be downloaded directly to your computer", style={
            'fontSize': '0.9rem',
            'color': COLORS['secondary'],
            'textAlign': 'center',
            'fontStyle': 'italic'
        })
    ], style={
        'padding': '20px',
        'backgroundColor': '#f8fafc',
        'borderRadius': '8px',
        'marginTop': '25px'
    })