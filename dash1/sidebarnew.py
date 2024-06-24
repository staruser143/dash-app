import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from layouts.layout1 import layout1
from layouts.layout2 import layout2


# Create the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

from callbacks.callback1 import register_callbacks1
from callbacks.callback2 import register_callbacks2
register_callbacks1(app)
register_callbacks2(app)

# Define the app layout with a sidebar and content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Layout 1', href='/layout1'),
        html.Br(),
        dcc.Link('Layout 2', href='/layout2'),
    ], style={'padding': 10, 'flex': 1}),
    html.Div(id='page-content', style={'padding': 10, 'flex': 4})
])


# Callback to update the content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/layout1':
        return layout1
    elif pathname == '/layout2':
        return layout2
    else:
        return '404'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)