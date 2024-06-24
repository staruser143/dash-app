from dash import html,dash_table
import pandas as pd
import filterui
from filterui import layout

    
# Initialize the DataTable with empty data and enable sorting
layout = html.Div([
    filterui.layout,
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
        #sort_mode='multi',  # Allow sorting by multiple columns
        sort_by=[]  # Initialize sort_by to an empty list
    )
])


