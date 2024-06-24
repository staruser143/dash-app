import dash
from dash import Dash, html,dcc
from dash.dependencies import Input, Output

from pages import home,about,contact,datatable,filterui
  
from callbacks import callback1,callback2,datatable_callback



app= Dash(__name__)
server=app.server
app.config.suppress_callback_exceptions=True
callback1.register_callbacks1(app)
callback2.register_callbacks2(app)
datatable_callback.register_datatable_callback(app)


app.layout=html.Div( [ 
    dcc.Location(id='url',refresh=False),
    html.Div([
        dcc.Link('Home',href='/',style={'padding':'10px'}),
        dcc.Link('About',href='/about',style={'padding':'10px'}),
        dcc.Link('Contact',href='/contact',style={'padding':'10px'}),
        dcc.Link('datatable',href='/datatable',style={'padding':'10px'})
    ]),
    html.Div(id='page-content')
])
# Update page-content based on URL
@app.callback(Output('page-content','children'),
              [Input('url','pathname')])
def display_page(pathname):
    if pathname=='/about':
        return about.layout
    elif pathname=='/contact':
        return contact.layout
    elif pathname=='/datatable':
        return datatable.layout
    else:
        return home.layout

# Start dash server
if __name__ == "__main__":
    app.run_server(debug=True)

   