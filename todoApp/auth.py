from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_hashed_password(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session=Depends(get_db)):
    create_users_model = models.Users()
    create_users_model.email = create_user.email
    create_users_model.username = create_user.username
    create_users_model.first_name = create_user.first_name
    create_users_model.last_name = create_user.last_name

    hash_password = get_hashed_password(create_user.password)

    create_users_model.hashed_password = hash_password
    create_users_model.is_active = True

    db.add(create_users_model)
    db.commit()

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username,  form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return "User Validated"







