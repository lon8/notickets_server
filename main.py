import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
import asyncio

from database.crud import router
from modules.logger import configure_logger
from modules.funcs import run_periodicaly, periodic_task
from database.ai.group import run_clustering


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

async def main():
    # interval = 300  # Интервал в секундах (5 минут)
    
    # # Запуск фоновой задачи
    # await start_tasks(interval, run_clustering)

    # Запуск Uvicorn сервера
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    await server.serve()

if __name__ == '__main__':
    configure_logger()
    
    asyncio.run(main())
