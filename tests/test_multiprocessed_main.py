import sys 
sys.path.append("/Users/imac/Desktop/projects/ai-stream/src")

import multiprocessing as mp
import asyncio 
import sys 

from utils import dialog_generation, video_streaming, clean_app
from donation.database.models import async_create_tables
from donation.server import run_server 


async def async_generation_coro() -> None:
    await async_create_tables()
    await dialog_generation()


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
        run_server() 

    elif choice == "2" or not choice:
        processes = [mp.Process(target=start_async_generation),
                       mp.Process(target=video_streaming)]

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