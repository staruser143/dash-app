from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,declarative_base

Base = declarative_base()

# Assuming a simple User and Table model for demonstration
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class UserTableAccess(Base):
    __tablename__ = 'user_table_access'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    table_name = Column(String)

# Setup DB connection
engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Your Dash app setup follows here
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import sqlalchemy as sa

# Initialize Dash app
app = dash.Dash(__name__)

# Assuming you have a function to get table names and user names
def get_table_names():
    # This function would fetch table names from your database
    return ['table1', 'table2', 'table3']

def get_user_names():
    # This function would fetch user names from your database
    return [{'label': 'User 1', 'value': 1}, {'label': 'User 2', 'value': 2}]

app.layout = html.Div([
    dcc.Dropdown(
        id='tables-dropdown',
        options=[{'label': table, 'value': table} for table in get_table_names()],
        multi=True
    ),
    dcc.Dropdown(
        id='users-dropdown',
        options=get_user_names()
    ),
    html.Button('Submit', id='submit-btn', n_clicks=0),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('submit-btn', 'n_clicks')],
    [State('tables-dropdown', 'value'), State('users-dropdown', 'value')]
)
def update_output(n_clicks, selected_tables, selected_user):
    if n_clicks > 0:
        # Here you would insert the selected tables and user into the database
        session = Session()
        for table in selected_tables:
            access_record = UserTableAccess(user_id=selected_user, table_name=table)
            session.add(access_record)
        session.commit()
        return f'User {selected_user} has been granted access to {", ".join(selected_tables)}'
    return 'Select tables and a user, then click submit.'

if __name__ == '__main__':
    app.run_server(debug=True)