#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Depends, FastAPI

from app.dependencies import get_token_header, get_current_active_user
from app.internal import admin
from app.routers import items, users, token

app = FastAPI(title="Auth Service", version="1.0.0")

app.include_router(token.router)
app.include_router(users.router, dependencies=[
                   Depends(get_current_active_user)])
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
