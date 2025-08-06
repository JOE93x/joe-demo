from fastapi import FastAPI
from config import Base,engine
from routes import router

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Basic joe User CRUD API")

app.include_router(router)