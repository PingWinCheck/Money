from fastapi import FastAPI, status, Request
import uvicorn
from auth.router import router as auth_router
from fastapi.staticfiles import StaticFiles
from core.log import get_logger
from fastapi.responses import JSONResponse
from catalog.routers import router as catalog_router, router_v2 as catalog_router_v2
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    logger.error("[METHOD=%s], [URL=%s], EXCEPTION=%s",
                 request.method, request.url, exc)
    return JSONResponse(content={'message': 'Произошла ошибка на сервере'},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(catalog_router_v2)

static = StaticFiles(directory='static')
app.mount('/static', static)


@app.get('/')
def home():
    return 'Home Page'


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
