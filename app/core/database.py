# import asyncio

# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from asyncio import current_task

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:p4ssw0rd@127.0.0.1:3306/shoppingcartapp"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# loop = asyncio.get_event_loop()
# yield loop
# loop.close()
Base = declarative_base()

# SessionLocal = async_scoped_session(
#     sessionmaker(
#         autocommit=False,
#         autoflush=True,
#         bind=engine,
#         class_=AsyncSession,
#     ),
#     scopefunc=current_task,
# )

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# We should disable the "expire on commit" behavior of sessions with expire_on_commit=False.
# This is because in async settings, we don't want SQLAlchemy to issue new SQL queries to
# the database when accessing already committed objects.

