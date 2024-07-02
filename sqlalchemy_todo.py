
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from models.mymodels import UserTableAccess,  SessionLocal


# Your Dash app setup follows here


# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Assuming you have a function to get table names and user names
def get_table_names():
    # This function would fetch table names from your database
    return ['table1', 'table2', 'table3']

def get_user_names():
    # This function would fetch user names from your database
    return [{'label': 'User 1', 'value': 1}, {'label': 'User 2', 'value': 2}]

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Tables", html_for="tables-dropdown"),
            dcc.Dropdown(
                id='tables-dropdown',
                options=[{'label': table, 'value': table} for table in get_table_names()],
                multi=True
            ),
        ], width=6),
        dbc.Col([
            dbc.Label("Select User", html_for="users-dropdown"),
            dcc.Dropdown(
                id='users-dropdown',
                options=get_user_names()
            ),
        ], width=6),
    ]),
    dbc.Button('Submit', id='submit-btn', className="mt-3"),
    dbc.Alert(id="success-alert", children="", color="success", is_open=False,duration=5000),

])
@app.callback(
    [Output('success-alert', 'children'),
     Output('success-alert', 'is_open')],
    [Input('submit-btn', 'n_clicks')],
    [State('tables-dropdown', 'value'), State('users-dropdown', 'value')]
)
def update_output(n_clicks, selected_tables, selected_user):
    # Provide a default value of 0 if n_clicks is None
    n_clicks = n_clicks or 0
    if n_clicks > 0:
        # Here you would insert the selected tables and user into the database
        session = SessionLocal()
        for table in selected_tables:
            # Check if the user already has access to the table
            existing_access = session.query(UserTableAccess).filter_by(user_id=selected_user, table_name=table).first()
            if not existing_access:
                access_record = UserTableAccess(user_id=selected_user, table_name=table)
                session.add(access_record)
            else:
                # Optionally, you can add a message indicating that the user already has access to this table
                print(f"User {selected_user} already has access to {table}.")
                success_message = f'User {selected_user} already has access to {table}.'
                return success_message, True
        session.commit()
        # Ensure selected_tables is an iterable of strings
        if isinstance(selected_tables, str):
            selected_tables = [selected_tables]  # Convert to list if it's a single string
        elif not isinstance(selected_tables, (list, tuple, set)):
            selected_tables = []  # Set to an empty list or handle appropriately if it's not an expected type

        success_message = f'Success! User {selected_user} has been granted access to {", ".join(selected_tables)}'
        # Update the alert message and make it visible
        return success_message, True
       # return f'User {selected_user} has been granted access to {", ".join(selected_tables)}'
    return  '', False

if __name__ == '__main__':
    app.run_server(debug=True)