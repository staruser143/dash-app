from dash import Output, Input


def register_callbacks1(app):
    @app.callback(
        Output('demo1', 'children'),  # Target the Graph component by its ID
        [Input('input1-dropdown', 'value')]  # Assume there's an input component with this ID
    )
    def update_graph(selected_value):
        print(f'Received value: { selected_value}')
        #val={selected_value}
        return selected_value

    