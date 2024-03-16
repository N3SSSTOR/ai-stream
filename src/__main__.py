from threading import Thread 
import asyncio 

from utils import dialog_generation, video_streaming 
from donation.database.models import async_create_tables
from donation.server import run_server 


async def async_start_generation() -> None:
    await async_create_tables()
    await dialog_generation()


def async_main() -> None:
    asyncio.run(async_start_generation())


def main():
    thread_1 = Thread(target=async_main)
    thread_2 = Thread(target=video_streaming)
    thread_3 = Thread(target=run_server)

    thread_1.start()
    thread_2.start()
    thread_3.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()


if __name__ == "__main__":
    try:
        main()
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        print("\nExit") 