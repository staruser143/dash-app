dash_table.DataTable(
    id='access-records-table',
    columns=[
        {"name": "User ID", "id": "user_id"},
        {"name": "Table Name", "id": "table_name"},
        # Add a column for the delete action
        {"name": "", "id": "delete", "deletable": False, "selectable": False}
    ],
    data=fetch_access_records(),  # Assuming this function fetches the current access records
    row_deletable=False,  # Ensure this is set to False
    editable=False,  # Ensure this is set to False
    # Add a column for the delete button
    style_data_conditional=[
        {
            'if': {'column_id': 'delete'},
            'textAlign': 'center',
            'padding': '0',
        }
    ],
    # Generate the delete button for each row
    data=[{**row, 'delete': 'X'} for row in fetch_access_records()],
)

from dash.exceptions import PreventUpdate

@app.callback(
    Output('access-records-table', 'data'),
    [Input('access-records-table', 'active_cell')],
    [State('access-records-table', 'data')]
)
def delete_access_record(active_cell, rows):
    if not active_cell or active_cell['column_id'] != 'delete':
        raise PreventUpdate
    row_to_delete = rows[active_cell['row']]
    user_id = row_to_delete['user_id']
    table_name = row_to_delete['table_name']
    
    # Perform the deletion from the database
    session = SessionLocal()
    access_record = session.query(UserTableAccess).filter_by(user_id=user_id, table_name=table_name).first()
    if access_record:
        session.delete(access_record)
        session.commit()
    session.close()
    
    # Remove the row from the data
    rows.pop(active_cell['row'])
    return rows

