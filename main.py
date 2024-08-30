from fastapi import FastAPI, status, Request
import uvicorn
from auth.router import router as auth_router
from fastapi.staticfiles import StaticFiles
from core.log import get_logger
from fastapi.responses import JSONResponse

logger = get_logger()

app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    logger.error("[METHOD=%s], [URL=%s], EXCEPTION=%s",
                 request.method, request.url, exc)
    return JSONResponse(content={'message': 'Произошла ошибка на сервере'},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


app.include_router(auth_router)
static = StaticFiles(directory='static')
app.mount('/static', static)


@app.get('/')
def home():
    return 'Home Page'


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
