import asyncio 

from utils import dialog_generation


async def main() -> None:
    await dialog_generation()
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExit") 