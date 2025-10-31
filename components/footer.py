from dash import html


def create_footer():
    """Create a footer for the application."""
    footer = html.Footer([
        html.Hr(),
        html.P("© 2025 Course Bidding Dashboard", 
               className="text-center text-muted")
    ], className="mt-5")
    return footer
