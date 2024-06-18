import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dbc.Progress(id="my-progress-bar", value=0, striped=True, animated=True),
    Input('submit-button', 'n_clicks')
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