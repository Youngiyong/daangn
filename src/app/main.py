import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.router import router
from app.db import database

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router, prefix=settings.API_V1_STR+"/votes", tags=['votes'])

if __name__ == "__main__":
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True, debug=True)
