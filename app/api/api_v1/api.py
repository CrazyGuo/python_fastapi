from fastapi import APIRouter

from app.api.api_v1.endpoints import login, schema

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])

type_defs = schema.type_defs
user_query = login.user_query

