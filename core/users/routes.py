from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from users.schemas import *
from users.models import UserModel
from core.database import get_db
from sqlalchemy.orm import Session
import secrets
from auth.jwt_auth import (
    ACCESS_TOKEN_COOKIE_NAME,
    REFRESH_TOKEN_COOKIE_NAME,
    decode_refresh_token,
    generate_access_token,
    generate_refresh_token,
)
from core.config import settings


router = APIRouter(tags=['users'], prefix='/users')


def generate_token():
    return secrets.token_hex(32)


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )


def delete_auth_cookies(response: Response):
    response.delete_cookie(key=ACCESS_TOKEN_COOKIE_NAME)
    response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME)


@router.post('/login')
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(
        username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='user dosent exist')
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='password is invalid')


    response = JSONResponse(content={'detail': 'logged in successfully'})
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    set_auth_cookies(response, access_token, refresh_token)
    return response


@router.post('/register')
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='username already exists')
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(content={'detail': 'user registered successfully'})


@router.post('/refresh-token')
async def user_refresh_token(request: Request):
    refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='refresh token cookie not found',
        )

    user_id = decode_refresh_token(refresh_token)
    access_token = generate_access_token(user_id)
    new_refresh_token = generate_refresh_token(user_id)

    response = JSONResponse(content={'detail': 'session renewed successfully'})
    set_auth_cookies(response, access_token, new_refresh_token)
    return response


@router.post('/logout')
async def user_logout():
    response = JSONResponse(content={'detail': 'logged out successfully'})
    delete_auth_cookies(response)
    return response
