from dash import Dash
import dash_bootstrap_components as dbc
from layouts import create_table_layout  
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up the layout
app.layout = create_table_layout()
register_callbacks(app)  # Register the callbacks

if __name__ == '__main__':
    app.run_server(debug=True)