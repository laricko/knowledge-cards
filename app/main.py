from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from routers import api_router


settings = get_settings()


def create_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_TITLE)
    app.add_middleware(
        CORSMiddleware,
        allow_origins="origins",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app


app = create_application()


@app.on_event("startup")
async def startup():
    print("startup...")


@app.on_event("shutdown")
async def shutdown():
    print("shutdowning...")


if __name__ == "__main__":
    run(
        "main:app",
        port=settings.SITE_PORT,
        host=settings.SITE_HOST,
        reload=True,
        forwarded_allow_ips="*",
        workers=4
    )
