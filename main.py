from fastapi import FastAPI, Depends
import models
from database import engine
from typing import Optional
from starlette.staticfiles import StaticFiles

from routers import auth, todos, address


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/statis", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(address.router)

