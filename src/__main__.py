import asyncio 

from utils import dialog_generation
from donation.database.models import async_create_tables


async def main() -> None:
    await async_create_tables()
    await dialog_generation()
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.exceptions.CancelledError:
        print("\nExit") 