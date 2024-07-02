import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

# Assuming a DataFrame or similar structure to hold permissions
permissions_df = pd.DataFrame(columns=['user', 'tables'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('User Authorization Management'),
    dcc.Dropdown(id='user-dropdown', multi=False, placeholder='Select User'),
    dcc.Dropdown(id='table-dropdown', multi=True, placeholder='Select Tables'),
    html.Button('Add Permission', id='add-permission-btn', n_clicks=0),
    html.Button('Revoke Permission', id='revoke-permission-btn', n_clicks=0),
    dash_table.DataTable(id='permissions-table', columns=[
        {'name': 'User', 'id': 'user'},
        {'name': 'Tables', 'id': 'tables'}
    ]),
    dcc.ConfirmDialog(id='confirm-dialog')
])

# Sample data for users and tables
users_data = pd.DataFrame({'user_id': [1, 2, 3], 'user_name': ['Alice', 'Bob', 'Charlie']})
tables_data = ['Table1', 'Table2', 'Table3']


def get_users():
    # Replace with actual DB call
    return pd.DataFrame({'user_id': [1, 2, 3], 'user_name': ['Alice', 'Bob', 'Charlie']})

def get_tables():
    # Replace with actual DB call
    return ['Table1', 'Table2', 'Table3']

@app.callback(
    Output('user-dropdown', 'options'),
    Output('table-dropdown', 'options'),
    Input('user-dropdown', 'id')
)
def update_dropdowns(_):
    user_options = [{'label': row['user_name'], 'value': row['user_id']} for _, row in users_data.iterrows()]
    table_options = [{'label': table, 'value': table} for table in tables_data]
    return user_options, table_options




@app.callback(
    Output('permissions-table', 'data'),
    Input('add-permission-btn', 'n_clicks'),
    Input('confirm-dialog', 'submit_n_clicks'),
    State('user-dropdown', 'value'),
    State('table-dropdown', 'value'),
    State('permissions-table', 'data')
)
def manage_permissions(add_clicks, confirm_clicks, selected_user, selected_tables, current_data):
    global permissions_df

    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if not selected_user or not selected_tables:
        return current_data

    if button_id == 'add-permission-btn' and add_clicks > 0:    
        new_rows = []  # Collect new rows here
        # Add permissions
        for table in selected_tables:
            #permissions_df = permissions_df.append({'user': selected_user, 'tables': table}, ignore_index=True)
            
            new_rows.append({'user': selected_user, 'tables': table})
            # Convert the list of new rows to a DataFrame and then concatenate
            new_rows_df = pd.DataFrame(new_rows)
            permissions_df = pd.concat([permissions_df, new_rows_df], ignore_index=True)
           # new_rows_df = pd.DataFrame(new_rows)
    elif button_id == 'confirm-dialog' and confirm_clicks > 0:
        # Revoke permissions
        permissions_df = permissions_df[~((permissions_df['user'] == selected_user) & (permissions_df['tables'].isin(selected_tables)))]

    elif button_id == 'revoke-permission-btn':
        # Revoke permissions
        permissions_df = permissions_df[~((permissions_df['user'] == selected_user) & (permissions_df['tables'].isin(selected_tables)))]

    # Convert DataFrame to a list of dictionaries for DataTable
    data = permissions_df.to_dict('records')
    return data

# Confirm dialog for revoking permissions
@app.callback(
    Output('confirm-dialog', 'displayed'),
    Input('revoke-permission-btn', 'n_clicks')
)
def display_confirm(n_clicks):
    if n_clicks > 0:
        return True
    return False

if __name__ == '__main__':
    app.run_server(debug=True)
