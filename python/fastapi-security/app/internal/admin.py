#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
