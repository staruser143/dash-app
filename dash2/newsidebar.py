# Import necessary libraries
import dash
from dash import dcc,html

from dash.dependencies import Input, Output

from pages import about, contact, home
from callbacks import callback1, callback2


# Create a Dash application
app = dash.Dash(__name__)
server=app.server
app.config.suppress_callback_exceptions = True
callback1.register_callbacks1(app)
callback2.register_callbacks2(app)

# Define the style for the sidebar
sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# Define the style for the content area
content_style = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}

# Define the style for the NavBar
navbar_style = {
    'background-color': 'grey',  # Bootstrap primary color
    'padding': '10px 0',
    'color': 'white',
    'width': '100%',
    'position': 'fixed',
    'z-index': '999'
}


# Define the style for the right-aligned link container
right_link_container_style = {
    'display': 'flex',
    'justify-content': 'flex-end',  # Aligns content to the right
    'align-items': 'center',  # Vertically centers the links
    'padding-right': '20px'  # Adds some spacing from the right edge
}

# Create the user options links
user_options = html.Div([
    dcc.Link('View Profile', href='/profile', style={'color': 'white', 'padding-right': '15px'}),
    dcc.Link('Sign Out', href='/logout', style={'color': 'white'}),
], style=right_link_container_style)

# Define the logo style (optional, adjust as needed)
logo_style = {
    'height': '50px',  # Adjust the height to fit your NavBar
    'padding': '5px',  # Adds some padding around the logo
}

# Update the navbar layout to include the logo
navbar1= html.Div(
    [
        html.Img(src='/assets/bird_2.jpg', style=logo_style),  # Update the src path to your logo
        html.H2('Demo Application', style={'textAlign': 'center', 'color': 'white'}),
        # The rest of your NavBar content here
    ],
    style=navbar_style
)

# Create the NavBar layout
navbar = html.Div(
    [
        html.H2('Demo Application', style={'textAlign': 'center', 'color': 'white'}),
       # user_options # Add more navigation items or buttons here as needed
    ],
    style=navbar_style
)
# Define the sidebar layout
sidebar = html.Div(
    [
        html.H2('Navigation', style={'textAlign': 'center'}),
        html.Hr(),
        #html.P('A simple sidebar layout with navigation links', className='lead'),
        dcc.Location(id="url", refresh=False),
        html.Div([
            dcc.Link('Home', href='/', style={'padding': '10px'}),
            dcc.Link('US States', href='/usstates', style={'padding': '10px'}),
            dcc.Link('Indian States', href='/indianstates', style={'padding': '10px'}),
        ], style={'display': 'flex', 'flexDirection': 'column'}),
    ],
    style=sidebar_style,
)

# Define the main content area
content = html.Div(id='page-content', style=content_style)

# Combine sidebar and content into the app layout
app.layout = html.Div([
    #navbar,
     html.Div([sidebar, content], style={'margin-top': '10px'})  # Adjust margin-top based on the height of your navbar
])

# Callbacks to update the page content based on navigation
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/indianstates':
        return contact.layout
    elif pathname == '/usstates':
        return about.layout
    else:
        return home.layout
    # If the user tries to reach a different page, return a 404 message
    #return html.P("404 Page not found")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)