import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import page1
import page2

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

sidebar = dbc.Nav(
    [
        dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
        dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
    ],
    vertical=True,
    pills=True,
)

content = html.Div(id="page-content")

app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),
                dbc.Col(content),
            ]
        )
    ],
    fluid=True
)

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 3)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/page-{i}" for i in range(1, 3)]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page1.layout
    elif pathname == "/page-2":
        return page2.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == "__main__":
    app.run_server(port=8888)