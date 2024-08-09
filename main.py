from fastapi import FastAPI
import uvicorn
from auth.router import router as auth_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.include_router(auth_router)
static = StaticFiles(directory='static')
app.mount('/static', static)


@app.get('/')
def home():
    return 'Home Page'


# if __name__ == '__main__':
#     uvicorn.run("main:app", reload=True)
