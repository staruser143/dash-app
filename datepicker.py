import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import datetime

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.DatePickerSingle(
        id='my-date-picker',
        date=datetime.datetime.today()
    ),
    html.Div(id='date-picker-output-container')
])

@app.callback(
    Output('date-picker-output-container', 'children'),
    Input('my-date-picker', 'date')
)
def update_output(selected_date):
    return f'You have selected: {selected_date}'


if __name__ == '__main__':
    app.run_server(debug=True)
    