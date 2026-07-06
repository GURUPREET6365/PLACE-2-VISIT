from app.routers.places.models import Place
from app.routers.users.models import User
from app.routers.votes_ratings_feedback.models import Feedback, Ratings, Votes
from sqlalchemy import String, cast, or_


class AdminPanelDbOps:
    def __init__(self, db):
        self.db = db

    def all_place_query(self):
        return self.db.query(Place).all()

    def search_place(self, search_query):
        place = []
        for query in search_query:
            search_pattern = f"%{query}%"
            place_search = self.db.query(Place).filter(
                or_(
                    Place.place_name.ilike(search_pattern),
                    Place.about_place.ilike(search_pattern),
                    Place.place_address.ilike(search_pattern),
                    cast(Place.pincode, String).ilike(search_pattern)
                )
            ).limit(20).all()
            place.extend(place_search)

        return place

    def all_user_query(self):
        return self.db.query(User).all()

    def search_user(self, search_query):
        user = []
        for query in search_query:
            search_pattern = f"%{query}%"
            user_search = self.db.query(User).filter(
                or_(
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    cast(User.google_sub, String).ilike(search_pattern)
                )
            ).limit(20).all()
            user.extend(user_search)

        return user

    def all_votes_query(self):
        return self.db.query(Votes).all()

    def all_ratings_query(self):
        return self.db.query(Ratings).all()

    def all_feedback_query(self):
        return self.db.query(Feedback).all()
