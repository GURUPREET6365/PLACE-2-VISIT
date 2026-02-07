from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = ['*']

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

from .routers import user, places, auth, votes
app.include_router(places.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
