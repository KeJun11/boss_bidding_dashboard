import dash_bootstrap_components as dbc
from dash import dcc, html


def create_main_layout():
    """Create the main layout for the bidding dashboard."""
    
    layout = dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("Course Bidding Dashboard", className="text-center mb-4"),
                html.Hr()
            ])
        ]),
        
        # Top Section - All Main Filters Stacked Vertically
        dbc.Row([
            dbc.Col([
                # School/Department
                html.Label("School/Department:", className="form-label"),
                dcc.Dropdown(
                    id='school-department-dropdown',
                    placeholder="Select school/department",
                    searchable=True,
                    clearable=True,
                    className="mb-3"
                ),
                
                # Search Course
                html.Label("Search Course:", className="form-label"),
                dcc.Dropdown(
                    id='course-dropdown',
                    placeholder="Type or select a course (e.g., CS102)",
                    searchable=True,
                    clearable=True,
                    className="mb-3"
                ),
                
                # Bidding Window
                html.Label("Bidding Window:", className="form-label"),
                dcc.Dropdown(
                    id='bidding-window-dropdown',
                    placeholder="Select bidding window",
                    clearable=True,
                    className="mb-3"
                ),
                
                # Instructor
                html.Label("Instructor:", className="form-label"),
                dcc.Dropdown(
                    id='instructor-dropdown',
                    placeholder="Select instructor",
                    clearable=True,
                    className="mb-4"
                ),
            ], width=12, className="main-filters")
        ]),
        
        # Bottom Row - Sections and Charts
        dbc.Row([
            # Sections Filter Column
            dbc.Col([
                html.H5("Additional Filters", className="mb-3"),
                
                # Sections
                html.Label("Sections:", className="form-label"),
                dbc.Checklist(
                    id='sections-checklist',
                    options=[],
                    value=[],
                    className="mb-3"
                ),
                
            ], width=3, className="sections-filters"),
            
            # Charts Section
            dbc.Col([
                html.Div(id='charts-container')
            ], width=9)
        ])
    ], fluid=True)
    
    return layout
