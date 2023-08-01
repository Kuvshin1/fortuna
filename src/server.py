import uvicorn

from src.config import get_settings


def start():
    setting = get_settings()
    uvicorn.run(
        "src.main:app",
        host=setting.host,
        port=setting.port,
        reload=True
    )


if __name__ == "__main__":
    start()
