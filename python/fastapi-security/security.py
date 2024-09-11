#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi.security import OpenIdConnect
from fastapi import Depends, FastAPI

oidc = OpenIdConnect(
    openIdConnectUrl="http://localhost:8080/realms/tools/.well-known/openid-configuration")


app = FastAPI(swagger_ui_init_oauth={"clientId": "docs",
                                     "appName": "Doc Tools",
                                     "usePkceWithAuthorizationCodeGrant": True,
                                     "scopes": "openid profile", })


@app.get("/foo")
async def read_foo(token=Depends(oidc)):
    return token
