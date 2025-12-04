from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column
from sqlalchemy import Integer, JSON
from dotenv import load_dotenv
import os

load_dotenv()

PG_DNS = f'postgresql+asyncpg://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@localhost:5432/{os.getenv('NAME_DB')}'
engine = create_async_engine(PG_DNS)
DbSession = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    json: MappedColumn[dict] = mapped_column(JSON)

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()