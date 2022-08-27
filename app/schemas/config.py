from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
