import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import page1
import page2

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page1.layout
    elif pathname == '/page-2':
        return page2.layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)