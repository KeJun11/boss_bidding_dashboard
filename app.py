import dash
import dash_bootstrap_components as dbc
from layouts.main_layout import create_main_layout
from components.navbar import create_navbar
from components.footer import create_footer


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set app title
app.title = "Course Bidding Dashboard"

# Create the app layout
app.layout = dbc.Container([
    create_navbar(),
    create_main_layout(),
    create_footer()
], fluid=True)

# Import callbacks (this must be after app creation)
import callbacks.filtering

if __name__ == '__main__':
    app.run(debug=True)
