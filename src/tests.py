import asyncio 

from donation.utils import get_donations
from donation.database._requests import add_processed_donation, get_processed_donations


async def main() -> None:
    result = await get_donations()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())