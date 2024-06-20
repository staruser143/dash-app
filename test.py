layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pd.DataFrame().columns],
        data=[],
        style_table={'overflowX': 'auto'},  # Add a horizontal scrollbar
        page_action='custom',
        page_current=0,
        page_size=10,
        page_count=1,  # Initialize page_count to 1
        sort_action='custom',  # Enable sorting
        filter_action="custom",
        style_data_conditional=[
            {
                'if': {'state': 'hover'},  # 'state' can be 'active', 'selected', or 'hover'
                'backgroundColor': 'rgb(210, 210, 210)',
                'border': '1px solid rgb(255, 255, 255)'
            }
        ]
    )
])