from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 

from config import DB_CONNECTION_URL, ECHO

engine = create_async_engine(DB_CONNECTION_URL, echo=ECHO)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass 


class TokenPair(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str]
    refresh_token: Mapped[str]


class ProcessedDonation(Base):
    __tablename__ = "processed_donations"

    id: Mapped[int] = mapped_column(primary_key=True)
    donation_id: Mapped[int]


async def async_create_tables():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)