
from config.database import SessionLocal, engine, get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Auth
import os
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from routers import person, experience
from config.database import Base

load_dotenv()

# openssl rand -hex 32
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(person.router)
app.include_router(experience.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Auth
# def verify_password()
# def get_user(db, username: str):
#     user = db.query(models.User).filter(
#         models.User.username == username).first()
#     if not user:
#         return None
# def authenticate_user(db: Session, username: str, password: str):
#     user = fake_db.get(username)
#     if not user:
#         return False
#     return user["hashed_password"] == fake_hash_password(password)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# class UserInDB(User):
#     hashed_password: str
# def verify_password(password, person: models.Person):
#     return person.verify_password(password)
# def get_user(db, username: str):
#     user = crud.get_person_username(db, username)
#     if not user:
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password")
#     return user
# def authenticate_user(db: Session, username: str, password: str):
#     user = crud.get_person_username(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user):
#         return False
#     return user
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, os.getenv(
#         "SECRET_KEY"), algorithm=os.geten("ALGORITHM"))
#     return encoded_jwt
# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, os.getenv("SECRET_KEY"),
#                              algorithms=[os.getenv("ALGORITHM")])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = crud.get_person_by_username(db, username)
#     if user is None:
#         raise credentials_exception
#     return user
# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
# async def get_current_active_user(current_user: models.Person = Depends(get_current_user)):
#     return current_user
# @app.post("/token", response_model=schemas.Token)
# async def login(
#     # Change to user model
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password")
#     access_token_expires = timedelta(
#         minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}
# @app.get("/users/me")
# async def read_users_me(current_user: schemas.PersonGet = Depends(get_current_active_user)):
#     return current_user
# @app.get("/items")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}
# @app.post('/experience')
# async def create_experience(
#     experience: schemas.ExperienceCreate,
#     db: Session = Depends(get_db)
# ):
#     return crud.create_experience(db=db, experience=experience)
# @app.post("/create-person")
# async def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
#     return crud.create_person(db=db, person=person)
