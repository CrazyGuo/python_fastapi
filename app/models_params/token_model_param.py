from typing import Optional
from pydantic import BaseModel


class TokenModelParam(BaseModel):
    access_token: str
    token_type: str

