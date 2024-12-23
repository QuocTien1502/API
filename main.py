from fastapi import FastAPI
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from db import models
from db.database import engine
from routers import user, post, comment
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware
from db.config import settings

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)

while True:
    try:
        conn = psycopg2.connect(host = settings.database_hostname, database=settings.database_name,user=settings.database_username,password=settings.database_password_test_connect, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection succesfull!!")
        break
    except Exception as error:
        print("Connecting database fialed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "hello world"}

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)
app.mount('/images', StaticFiles(directory="images"), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

