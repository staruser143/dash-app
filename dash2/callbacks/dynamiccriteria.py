import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State, MATCH, ALL
import json
# Initialize Dash app
app = dash.Dash(__name__)

# Define initial layout
app.layout = html.Div([
    dcc.Store(id='conditions-store', data=[]),  # Store to keep track of active conditions
    html.Button('Add Condition', id='add-button', n_clicks=0),
    html.Div(id='conditions-container'),
    html.Button('Submit Query', id='submit-query', n_clicks=0),
    html.Pre(id='query-output')
])
from dash.exceptions import PreventUpdate
from dash import callback_context

@app.callback(
    Output('conditions-store', 'data'),
    [Input('add-button', 'n_clicks'),
     Input({'type': 'remove-button', 'index': ALL}, 'n_clicks')],
    [State('conditions-store', 'data')]
)
def update_conditions(add_clicks, remove_clicks_list, existing_conditions):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if 'add-button' in button_id:
        # Add a new condition. Use a unique identifier for each condition.
        new_condition_id = max(existing_conditions) + 1 if existing_conditions else 1
        return existing_conditions + [new_condition_id]
    else:
        # Remove the specified condition
        button_index = int(button_id.split('"index":')[1].rstrip('}'))
        if button_index in existing_conditions:
            return [cond for cond in existing_conditions if cond != button_index]

    return existing_conditions

# Callback to render conditions based on active indices in store
@app.callback(
    Output('conditions-container', 'children'),
    [Input('conditions-store', 'data')]
)
def render_conditions(data):
    children = []
    for index in data:
        children.append(html.Div([
            dcc.Dropdown(
                id={'type': 'field-dropdown', 'index': index},
                options=[
                    {'label': 'Field 1', 'value': 'field_1'},
                    {'label': 'Field 2', 'value': 'field_2'},
                    # Add more field options here
                ],
                placeholder="Select field"
            ),
            dcc.Dropdown(
                id={'type': 'operator-dropdown', 'index': index},
                options=[
                    {'label': '>', 'value': '<'},
                    {'label': '<', 'value': '>'},
                    # Add more field options here
                ],
                placeholder="Select operator"
            ),
            dcc.Input(id={'type': 'value-input', 'index': index}, type='text', placeholder="Value"),
            html.Button('Remove', id={'type': 'remove-button', 'index': index}, n_clicks=0)
        ], key=str(index)))  # Convert index to string))  # Use 'key' to ensure React can manage these dynamic components efficiently
    return children

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)