# app.py
from dash import Dash
import dash_bootstrap_components as dbc

def create_app():
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server

    from layouts.layout1 import layout1
    from layouts.layout2 import layout2
    from callbacks.callback1 import register_callbacks1
    from callbacks.callback2 import register_callbacks2

   
    use_layout1 = True

    if use_layout1:
        app.layout = layout1
        register_callbacks1(app)
    else:
        app.layout = layout2
        # Assuming you have a callback2 module for layout2
        register_callbacks2(app)

    return app

app = create_app()
if __name__ == "__main__":
    app.run_server(debug=True)