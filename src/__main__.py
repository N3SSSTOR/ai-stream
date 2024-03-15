from threading import Thread 
import asyncio 

from utils import dialog_generation, video_streaming 
from donation.database.models import async_create_tables


async def async_start_dialog() -> None:
    await async_create_tables()
    await dialog_generation()


def async_main() -> None:
    asyncio.run(async_start_dialog())


def main():
    thread_1 = Thread(target=async_main)
    thread_2 = Thread(target=video_streaming)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()


if __name__ == "__main__":
    try:
        main()
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        print("\nExit") 