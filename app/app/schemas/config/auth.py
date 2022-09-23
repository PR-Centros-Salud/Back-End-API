# Library Importation
from pydantic import BaseModel, validator
from typing import Optional, Union
from datetime import datetime, date


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
