from typing import Annotated
from fastapi import APIRouter, Form, Depends, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import UserCreate
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/auth', tags=['auth', 'user'])
template = Jinja2Templates('auth/templates')


@router.post('/register', response_model=UserCreate)
async def register(user: Annotated[UserCreate, Depends()]):
    return user


# frontend
@router.get('/login')
async def reg(request: Request):
    return template.TemplateResponse(request, 'login.html')
