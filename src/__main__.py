import threading 
import asyncio 

from utils import dialog_generation, video_streaming, clean_app
from donation.database.models import async_create_tables
from donation.server import run_server 


async def async_generation() -> None:
    await async_create_tables()
    await dialog_generation()


def start_async_generation() -> None:
    asyncio.run(async_generation())


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
        thread_pool = [threading.Thread(target=start_async_generation),
                       threading.Thread(target=video_streaming)]

        for thread in thread_pool:
            thread.start()
        
        for thread in thread_pool:
            thread.join()


if __name__ == "__main__":
    try:
        main()
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        print("\nExit") 