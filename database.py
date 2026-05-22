from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = 'postgresql://srikanth:12345@localhost:5432/fastapi_db'
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
