# app/main.py
from fastapi import FastAPI
from database import engine, Base
from routers import auth, user

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Auth Service is running"}