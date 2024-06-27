# Step 1: Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import html

# Step 2: Initialize the Dash app with a Bootstrap theme
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Step 3: Define the NavBar
navbar = dbc.NavbarSimple(
    brand="My App",
    brand_href="#",
    color="primary",
    dark=True,
)

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "width": "20%", 
        "height": "100vh", 
        "background-color": "#f8f9fa",
        "padding": "10px",
        "overflow-x": "hidden",  # Prevents horizontal overflow
        "overflow-y": "auto"  # Allows vertical scrolling if necessary
    },
)

# Additional global CSS for text overflow handling


# Add this CSS rule in the linked stylesheet or in your app's custom CSS
'''
.nav-link {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 15px;  # Adjust as necessary
}
'''


# Step 5: Define the layout with NavBar and Sidebar
app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),
                dbc.Col(html.Div("Content goes here"), width=10),
            ]
        ),
    ],
    fluid=True,
)

# Step 6: Run the app
if __name__ == "__main__":
    app.run_server(debug=True)