import multiprocessing as mp
import asyncio 
import sys 

from utils import async_dialog_generation, video_streaming, clean_app
from donation.database.models import async_create_tables
from donation.server import run_server 


async def async_generation_coro() -> None:
    await async_create_tables()
    await async_dialog_generation()


def start_async_generation() -> None:
    asyncio.run(async_generation_coro())


def main() -> None:
    clean_app()
    
    choice = input(
        "\nЧто запускаем?\n\n"
        "Сервер для авторизации в DonationAlerts - 1\n"
        "Процесс генерации видео и стриминга - 2 [*]\n\n"
        ">>> "
    )

    if choice == "1":
        asyncio.run(async_create_tables())
        run_server() 

    if choice == "2" or not choice:
        processes = [mp.Process(target=func) for func in [start_async_generation, video_streaming]]

        for process in processes:
            process.start()
        
        for process in processes:
            process.join()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nExit") 
        sys.exit()