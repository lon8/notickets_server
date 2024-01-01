import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handlers import router

origins = [
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "http://localhost:4200",
    "http://192.168.1.197"
]

def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application

app = get_application()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="info")