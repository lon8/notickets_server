import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.crud import router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


app = get_application()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5555, log_level="info")
