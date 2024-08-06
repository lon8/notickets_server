import asyncio
import time
from typing import Callable
import threading


async def periodic_task(interval: int, func: Callable[[], None]) -> None:
    """
    Асинхронная задача, которая запускает переданную функцию каждые interval секунд.

    :param interval: Интервал времени между запусками функции в секундах.
    :param func: Асинхронная функция, которую необходимо выполнять. Не принимает аргументов и не возвращает значения.
    """
    while True:
        await func()
        await asyncio.sleep(interval)
        
def run_periodicaly(interval :int, func: Callable [[], None]) -> None:
    """
    Запускает переданную функцию каждые interval секунд в отдельном потоке.

    :param interval: Интервал времени между запусками функции в секундах.
    :param func: Функция, которую необходимо выполнять. Не принимает аргументов и не возвращает значения.
    """
    def wrapper() -> None:
        while True:
            func()
            time.sleep(interval)
            
    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    
async def start_tasks(interval: int, func: Callable[[], None]) -> None:
    asyncio.create_task(periodic_task(interval, func))