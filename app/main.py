import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
#import graphene
#from starlette.graphql import GraphQLApp
#from .api.api_v1.endpoints.graphql_api import Query

from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from starlette.middleware.authentication import AuthenticationMiddleware

from app.middlewares.authentication import BasicAuthBackend
from app.api.api_v1.api import api_router, type_defs, user_query
from app.core.config import settings
from app.db_service.init_db import init_db_data


app = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

#用户登录信息检查拦截
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend() )

app.include_router(api_router, prefix=settings.API_V1_STR)
#测试GraphQL
#app.add_route("/gl", GraphQLApp(schema=graphene.Schema(query=Query)))
schema = make_executable_schema(type_defs, [user_query])
app.mount("/graphql", GraphQL(schema, debug=True))

def start_fast_api(init_db=True):
    if init_db:
        init_db_data()
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
