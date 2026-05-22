#from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


db_url = 'postgresql+asyncpg://srikanth:12345@localhost:5432/fastapi_db'
#engine = create_engine(db_url)
engine = create_async_engine(db_url, echo=True)
session = sessionmaker(autocommit=False, class_=AsyncSession, expire_on_commit=False, autoflush=False, bind=engine)
