import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str
    #如果Key是动态的生成，一旦服务器重启之后，之前生成的token就无法验证通过，所以最好保存下来
    #SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SERVER_NAME: str
    SERVER_HOST: str
    SERVER_PORT: int
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]

    @validator("BACKEND_CORS_ORIGINS", pre=True) #对env中的值进行处理 最终保存到BACKEND_CORS_ORIGINS中
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DB_SERVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: str

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool

    class Config:
        case_sensitive = True

app_dir = Path(__file__).resolve().parent.parent
env_path = "%s/%s" % (app_dir, "prod.env")

#去掉_env_file_encoding='utf-8' 因为在docker中报错
#settings = Settings(_env_file= env_path, _env_file_encoding='utf-8')
settings = Settings(_env_file= env_path)

