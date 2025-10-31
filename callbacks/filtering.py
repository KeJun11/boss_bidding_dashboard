from dash import Input, Output, State, callback, dcc, html
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
from utils.data_loader import (
    load_data, get_course_options, get_bidding_window_options,
    get_instructor_options, get_section_options, filter_data, sort_terms,
    get_school_department_options, get_all_terms
)

# Load data once
df = load_data()


@callback(
    Output('school-department-dropdown', 'options'),
    Input('school-department-dropdown', 'id')
)
def update_school_department_options(_):
    """Update school/department dropdown options."""
    return get_school_department_options(df)


@callback(
    Output('course-dropdown', 'options'),
    Input('school-department-dropdown', 'value')
)
def update_course_options(school_department):
    """Update course dropdown options based on school/department selection."""
    if school_department:
        filtered_df = df[df['School/Department'] == school_department]
        return get_course_options(filtered_df)
    return get_course_options(df)


@callback(
    Output('bidding-window-dropdown', 'options'),
    [Input('school-department-dropdown', 'value'),
     Input('course-dropdown', 'value')]
)
def update_bidding_window_options(school_department, course_code):
    """Update bidding window options based on school and course selection."""
    filtered_df = df.copy()
    if school_department:
        filtered_df = filtered_df[filtered_df['School/Department'] == school_department]
    if course_code:
        filtered_df = filtered_df[filtered_df['Course Code'] == course_code]
    return get_bidding_window_options(filtered_df)


@callback(
    Output('instructor-dropdown', 'options'),
    [Input('school-department-dropdown', 'value'),
     Input('course-dropdown', 'value'),
     Input('bidding-window-dropdown', 'value')]
)
def update_instructor_options(school_department, course_code, bidding_window):
    """Update instructor options based on school, course and bidding window selection."""
    filtered_df = df.copy()
    if school_department:
        filtered_df = filtered_df[filtered_df['School/Department'] == school_department]
    return get_instructor_options(filtered_df, course_code, bidding_window)


@callback(
    Output('sections-checklist', 'options'),
    [Input('school-department-dropdown', 'value'),
     Input('course-dropdown', 'value'),
     Input('bidding-window-dropdown', 'value'),
     Input('instructor-dropdown', 'value')]
)
def update_sections_options(school_department, course_code, bidding_window, instructor):
    """Update sections checklist based on all selections."""
    filtered_df = df.copy()
    if school_department:
        filtered_df = filtered_df[filtered_df['School/Department'] == school_department]
    return get_section_options(filtered_df, course_code, bidding_window, instructor)


@callback(
    Output('charts-container', 'children'),
    [Input('school-department-dropdown', 'value'),
     Input('course-dropdown', 'value'),
     Input('bidding-window-dropdown', 'value'),
     Input('instructor-dropdown', 'value'),
     Input('sections-checklist', 'value')]
)
def update_charts(school_department, course_code, bidding_window, instructor, sections):
    """Update charts based on filter selections."""
    
    if not course_code or not sections:
        return html.Div([
            html.H4("Please select a course and at least one section to view charts", 
                   className="text-center text-muted mt-5")
        ])
    
    # Filter data
    filtered_df = filter_data(df, school_department, course_code, bidding_window, instructor, sections)
    
    if filtered_df.empty:
        return html.Div([
            html.H4("No data available for the selected filters", 
                   className="text-center text-muted mt-5")
        ])
    
    # Get all possible terms for consistent x-axis
    all_terms = get_all_terms()
    all_terms_sorted = sort_terms(all_terms)
    
    # Create charts for each section - stack vertically in single column
    charts = []
    
    for section in sections:
        section_data = filtered_df[filtered_df['Section'] == section]
        
        if section_data.empty:
            continue
        
        # Group by term and calculate median and min bids
        chart_data = section_data.groupby('Term').agg({
            'Median Bid': 'mean',
            'Min Bid': 'mean'
        }).reset_index()
        
        # Create a complete dataframe with all terms, filling missing data with None
        complete_data = pd.DataFrame({'Term': all_terms_sorted})
        complete_data = complete_data.merge(chart_data, on='Term', how='left')
        
        # Sort terms chronologically
        complete_data['Term'] = pd.Categorical(complete_data['Term'], categories=all_terms_sorted, ordered=True)
        complete_data = complete_data.sort_values('Term')
        
        # Create the line chart
        fig = go.Figure()
        
        # Add Median Bid line
        fig.add_trace(go.Scatter(
            x=complete_data['Term'],
            y=complete_data['Median Bid'],
            mode='lines+markers',
            name='Median Bid',
            line=dict(color='blue', width=2),
            marker=dict(size=6),
            connectgaps=False  # Don't connect across missing data
        ))
        
        # Add Min Bid line
        fig.add_trace(go.Scatter(
            x=complete_data['Term'],
            y=complete_data['Min Bid'],
            mode='lines+markers',
            name='Min Bid',
            line=dict(color='red', width=2),
            marker=dict(size=6),
            connectgaps=False  # Don't connect across missing data
        ))
        
        # Update layout - now with full width available
        fig.update_layout(
            title=f"{course_code} - Section {section}",
            xaxis_title="Term",
            yaxis_title="Bid Amount",
            height=400,
            showlegend=True,
            template="plotly_white",
            margin=dict(l=40, r=40, t=60, b=40),
            autosize=True,  # Allow width to adjust to container
            font=dict(size=12)  # Larger font now that we have more space
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        # Create chart component - full width in single column
        chart_component = dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=fig,
                    config={
                        'displayModeBar': True,  # Show toolbar since we have more space
                        'responsive': True
                    },
                    style={
                        'height': '400px',
                        'width': '100%'
                    }
                )
            ], width=12)
        ], className="mb-4")
        
        charts.append(chart_component)
    
    return html.Div(charts)
