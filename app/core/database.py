from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:p4ssw0rd@127.0.0.1:3306/shoppingcartapp"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

"""
We should disable the "expire on commit" behavior of sessions with expire_on_commit=False.
This is because in async settings, we don't want SQLAlchemy to issue new SQL queries to
the database when accessing already committed objects.
"""
