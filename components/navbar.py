import dash_bootstrap_components as dbc
from dash import html


def create_navbar():
    """Create a navigation bar for the application."""
    navbar = dbc.NavbarSimple(
        brand="Course Bidding Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
        className="mb-4"
    )
    return navbar
