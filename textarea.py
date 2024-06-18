import dash
from dash import dcc, html  
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id='textarea-output-container'),
    dcc.Textarea(
        id='my-textarea',
        placeholder='Enter a value...',
        style={'width': '100%'}
    ),
    html.Button('Submit', id='submit-button', n_clicks=0)

])  # Initialize app.layout



from dash.dependencies import Input, Output




from dash.dependencies import Input, Output, State

@app.callback(
    Output('textarea-output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('my-textarea', 'value')
)
def update_output(n_clicks, textarea_value):
    if n_clicks > 0:
        return f'You have entered: {textarea_value}'
    
if __name__ == '__main__':
    app.run_server(debug=True)