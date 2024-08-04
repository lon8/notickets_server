import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from database.crud import router
from modules.logger import configure_logger
from modules.funcs import periodic_task
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

if __name__ == '__main__':
    configure_logger()
    
    interval = 300  # Интервал в секундах (5 минут)
    asyncio.create_task(periodic_task(interval, run_clustering))

    # Основной цикл событий
    asyncio.get_event_loop().run_forever()
    
    # Запускаем сервер
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="info")
