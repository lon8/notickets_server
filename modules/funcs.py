import asyncio
from typing import Callable


async def periodic_task(interval: int, func: Callable[[], None]) -> None:
    """
    Асинхронная задача, которая запускает переданную функцию каждые interval секунд.

    :param interval: Интервал времени между запусками функции в секундах.
    :param func: Асинхронная функция, которую необходимо выполнять. Не принимает аргументов и не возвращает значения.
    """
    while True:
        await func()
        await asyncio.sleep(interval)
