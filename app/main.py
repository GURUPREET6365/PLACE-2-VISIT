from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import googleAuth
from app.routers.places.api import router as placerouter
from app.routers.users.adminpanel.places import router as admin_places_router
from app.routers.users.adminpanel.users import router as admin_users_router
from app.routers.users.adminpanel.vote_rating_feedback import router as admin_activity_router
from app.routers.users.api import router as userrouter
from app.routers.votes_ratings_feedback.feedback import router as feedbackrouter
from app.routers.votes_ratings_feedback.ratings import router as ratingsrouter
from app.routers.votes_ratings_feedback.votes import router as votesrouter

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "http://127.0.0.1:5500",
    "http://localhost",
    "http://localhost:8080",
    "https://placeexplorer.kumargurupreet2008.workers.dev",
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

app.include_router(placerouter)
app.include_router(userrouter)
app.include_router(googleAuth.router)
app.include_router(votesrouter)
app.include_router(feedbackrouter)
app.include_router(ratingsrouter)
app.include_router(admin_places_router)
app.include_router(admin_users_router)
app.include_router(admin_activity_router)
