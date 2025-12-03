from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

PG_DNS = f'postgresql+asyncpg://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@localhost:5432/{os.getenv('NAME_DB')}'
engine = create_async_engine(PG_DNS)
DbSession = async_sessionmaker(bind=engine, expire_on_commit=False)
