from app.routers.places.models import Place
from app.routers.votes_ratings_feedback.models import Feedback, Ratings, Votes
from sqlalchemy import and_


class VoteRatingFeedbackDbOps:
    def __init__(self, db):
        self.db = db

    def place_query_with_id(self, place_id):
        return self.db.query(Place).filter(Place.id == place_id).first()

    def user_vote_query(self, user_id, place_id):
        return self.db.query(Votes).filter(
            and_(Votes.place_id == place_id, Votes.user_id == user_id)
        ).first()

    def create_vote(self, user_id, place_id, vote_value):
        vote = Votes(
            user_id=user_id,
            place_id=place_id,
            vote=vote_value
        )
        self.db.add(vote)
        self.db.commit()
        self.db.refresh(vote)
        return vote

    def update_vote(self, vote, vote_value):
        vote.vote = vote_value
        self.db.commit()
        return vote

    def user_rating_query(self, user_id, place_id):
        return self.db.query(Ratings).filter(
            and_(Ratings.user_id == user_id, Ratings.place_id == place_id)
        )

    def update_rating(self, ratings_query, request):
        ratings_query.update(request.model_dump(), synchronize_session=False)
        self.db.commit()

    def create_rating(self, request):
        rating = Ratings(**request.model_dump())
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def create_feedback(self, request):
        new_feedback = Feedback(**request.model_dump())
        self.db.add(new_feedback)
        self.db.commit()
        return new_feedback
