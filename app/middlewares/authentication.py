import jwt
import uuid
import datetime
from starlette.requests import Request
from starlette.authentication import AuthenticationBackend, AuthCredentials, BaseUser
from fastapi import Request, HTTPException

from app.core import security
from app.core.config import settings
from app.db_service import user_service


#包装函数 用来处理必须登录才能访问的接口
def authentication_required_gl(resolver):
    async def wrapper_func(source, info, **kwargs):
        request = info.context["request"]
        result = None
        if request.user.is_authenticated:
            kwargs["current_user_id"] = request.user.current_user_id
            result = await resolver(source, info, **kwargs)
        return result

    return wrapper_func

def authentication_required_route(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=400, detail="the user not login.")
    return request.user.current_user_id

#检查user_id是否存在数据库中
async def check_user_in_db(user_id, received_token):
    user = user_service.user.get(id = user_id)
    if user: # user.token == received_token:
        return True
    return False

#已登录的用户信息类
class AuthenticatedUser(BaseUser):
    def __init__(self, user_id, expires = 0.0):
        self.current_user_id = user_id
        self.expires = expires
        self.req_id = uuid.uuid4().hex

    @property
    def is_authenticated(self):
        return True

#未登录的用户信息类
class UnAuthenticatedUser(BaseUser):
    def __init__(self):
        self.req_id = uuid.uuid4().hex

    @property
    def is_authenticated(self):
        return False


#authenticates each request and provides an unique reuest id to each
class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        ret_value, token = None, None
        #1.先从从cookies中获取authorization字段,失败再从headers获取
        if "authorization" in request.cookies.keys() and request.cookies["authorization"]:
            token = request.cookies["authorization"]
        elif "authorization" in request.headers.keys() and request.headers["authorization"]:
            bear_token = request.headers["authorization"]
            bear, token = bear_token.split(' ')
        if token is not None: 
            #2.解码Authorization，获取对应的字典结果
            decoded_token = jwt.decode(token.encode(), settings.SECRET_KEY, algorithms=[security.ALGORITHM])
            #3.字典中用户对应的token是否在数据库中
            match_token = await check_user_in_db(decoded_token["id"], token)
            now = datetime.datetime.now()
            #4.token是否过期 并设置对应的返回类对象
            if match_token and now.timestamp() < decoded_token["expire"]:
                ret_value = AuthenticatedUser(
                    user_id=decoded_token["id"], expires=decoded_token["expire"]
                )
                '''
                await token_db.set_token(
                    ret_value.req_id,
                    token,
                    decoded_token["expire"]
                )
                '''
            else:
                ret_value = UnAuthenticatedUser()

        else:
            ret_value = UnAuthenticatedUser()
        #5.返回元组，表示用户登录与否的信息
        return AuthCredentials(["authenticated"]), ret_value