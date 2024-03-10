from sqlalchemy import insert, select, update 

from .models import TokenPair, ProcessedDonation, async_session


async def set_tokens(access_token: str, refresh_token: str) -> None:
    async with async_session() as session:
        tokens = await session.scalar(select(TokenPair))
        if not tokens:
            await session.execute(
                insert(TokenPair).values(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            )
            await session.commit()
            return 
        
        await session.execute(
            update(TokenPair).where(TokenPair.id == 1).values(
                access_token=access_token,
                refresh_token=refresh_token
            )
        )
        await session.commit()


async def get_tokens() -> dict:
    async with async_session() as session:
        tokens = await session.scalar(select(TokenPair))
        if tokens:
            return {
                "access": tokens.access_token,
                "refresh": tokens.refresh_token
            }
        

async def add_processed_donation(donation_id: int) -> None:
    async with async_session() as session:
        await session.execute(
            insert(ProcessedDonation).values(donation_id=donation_id)
        )
        await session.commit()


async def get_processed_donations() -> list:
    async with async_session() as session:
        donations = await session.scalars(select(ProcessedDonation))
        donations_list = [donation.donation_id for donation in donations]

        return donations_list 