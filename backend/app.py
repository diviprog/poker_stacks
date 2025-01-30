from fastapi import FastAPI # type: ignore
from routes import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)