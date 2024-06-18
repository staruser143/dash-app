from dash import dcc, html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            dbc.Progress(id="my-progress-bar", value=25, striped=True, animated=True),
            html.Button('Submit', id='submit-button', n_clicks=0)
        ]
    )
])

@app.callback(
    Output('my-progress-bar', 'value'),
    Input('submit-button', 'n_clicks')
)
def update_progress(n_clicks):
    # Replace this with your own logic to calculate progress
    progress = n_clicks * 10
    return progress

if __name__ == '__main__':
    app.run_server(debug=True)