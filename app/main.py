from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.database.database import Base
app = FastAPI()


Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost.tiangolo.com",
    "http://127.0.0.1:5500",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {'message':'Hey, Welcome to the p2v. You can make your own frontend by using this api.'}

from .routers import user, places, auth, votes, adminpanel, ratings
app.include_router(places.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

app.include_router(adminpanel.router)

app.include_router(ratings.router)