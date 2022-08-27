# Library Importantion
from fastapi import FastAPI, HTTPException, APIRouter
from cruds.experience import create_experience

router = APIRouter(
    prefix="/experience",
    tags=["Experiences"]
)
