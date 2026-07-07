from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    pass


def get_engine(url: str | None = None):
    db_url = url or settings.database_url
    return create_async_engine(db_url, echo=False)


def get_session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


engine = get_engine()
SessionLocal = get_session_factory(engine)


async def get_db():
    async with SessionLocal() as session:
        yield session


async def init_db(eng=None):
    target = eng or engine
    async with target.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
