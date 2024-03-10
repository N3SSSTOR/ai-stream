import asyncio 

from donation.utils import get_donation_alerts_list


async def main() -> None:
    result = await get_donation_alerts_list()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())