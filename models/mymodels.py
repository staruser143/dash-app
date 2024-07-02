from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base
import sqlalchemy as sa
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
SessionLocal = sessionmaker(bind=engine)
# Create tables if they don't exist
Base.metadata.create_all(engine)
