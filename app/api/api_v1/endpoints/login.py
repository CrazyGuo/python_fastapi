
from datetime import timedelta
from pydantic import EmailStr

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ariadne import QueryType

from app.core.config import settings
from app.core import security
from app.models_params import TokenModelParam, UserModelParam, UserUpdateModelParam
from app.db_service import user_service
from app.models.user import AppUsers
from app.middlewares.authentication import authentication_required_route, authentication_required_gl

from pydantic import BaseModel 

router = APIRouter()

@router.post("/login/access-token", response_model = TokenModelParam)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    #1.检查用户账号是否合法
    user = user_service.user.authenticate(logon_name=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user_service.user.is_available(user):
        raise HTTPException(status_code=400, detail="Inactive user") 
    #2.用户合法，生成token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(user.id, expires_delta=access_token_expires)
    #3.将用户id和token信息保存到数据库存储

    #4.返回token等信息到client端
    return {
        "access_token": token,
        "token_type": "bearer",
    }

class EchoArgs(BaseModel):    #继承BaseModel
    name:str    #定义一个字符串型参数

#该接口主要用来测试 current_user_id: str = Depends(authentication_required2)
@router.post("/user/list", dependencies=[Depends(authentication_required_route)])
def user_list(param:EchoArgs):
    return "Success Test"

user_query = QueryType()

@user_query.field("search")
@authentication_required_gl
async def resolve_search(_, info, **kwargs):
    keyword = kwargs.get("keyword", None)
    resp = {
        "name": "Alex",
        "sex": "M"
    }
    return resp

@router.get("/user/me", response_model = UserModelParam)
def read_user_me(current_user_id: int = Depends(authentication_required_route)):
    user = user_service.user.get(id = current_user_id);

    current_user_data = jsonable_encoder(user)
    current_user = UserModelParam(**current_user_data);
    '''
    current_user.id = user.id;
    current_user.is_available = user.is_available;
    current_user.is_superuser = True;
    current_user.email = user.email;
    current_user.full_name = user.full_name;
    '''
    return current_user


@router.put("/user/me", response_model=UserModelParam)
def update_user_me(
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user_id: int = Depends(authentication_required_route)
):
    current_user = user_service.user.get(id = current_user_id);
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdateModelParam(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = user_service.user.update(db_obj=current_user, obj_in=user_in)
    return user

@router.post("/reset-password/")
def reset_password(
    new_password: str = Body(...),
    current_user_id: int = Depends(authentication_required_route)
):
    current_user = user_service.user.get(id = current_user_id);
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdateModelParam(**current_user_data)
    if new_password is not None:
        user_in.password = new_password
    user = user_service.user.update(db_obj=current_user, obj_in=user_in)
    return {"msg": "Password updated successfully"}