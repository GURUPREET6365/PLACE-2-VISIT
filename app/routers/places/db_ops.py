from app.routers.places.models import Place
from sqlalchemy import and_, or_, cast, String
from app.routers.votes_ratings_feedback.models import Ratings, Votes

class PlacesDbOps:
    def __init__(self, db):
        self.db = db
    
    def get_only_db(self):
        return self.db
    
    def search_all_place(self, search_query):
        db = self.db
        place = []
        for all_query in search_query:
            search_pattern = f"%{all_query}%"
            place_search = db.query(Place).filter(or_(Place.place_name.ilike(search_pattern), (Place.about_place.ilike(search_pattern)), (Place.place_address.ilike(search_pattern)), (cast(Place.pincode, String).ilike(search_pattern)) )).limit(20).all()

            place.extend(place_search)
        
        return place
    
    def all_vote_query(self, place_id):
        db=self.db
        return db.query(Votes).filter(Votes.place_id == place_id).all()
    
    def all_place_query(self):
        db=self.db
        return db.query(Place).all()

    def is_voted_query(self, user_id, place_id):
        db=self.db
        return db.query(Votes).filter(and_(Votes.user_id==user_id, Votes.place_id==place_id)).first()
    
    def all_rated_place_query(self, place_id):
        db=self.db
        return db.query(Ratings).filter(Ratings.place_id == place_id).all()
    
    def is_user_rated_place_query(self, user_id, place_id):
        db=self.db
        return db.query(Ratings).filter(and_(Ratings.user_id==user_id, Ratings.place_id==place_id)).first()
    
    def create_place(self, request):
        db=self.db
        place = Place(**request.model_dump())
        db.add(place)
        db.commit()
        # This refresh is for when the data is returned, then it will first refresh db and then return so that all data should go and this store the data in place.
        db.refresh(place)
        return True
    
    def place_query_with_id(self, id):
        db=self.db
        return db.query(Place).filter(Place.id == id).first()
    
    def delete_query(self, db_row):
        db=self.db
        db.delete(db_row)
        db.commit()
        return True
    
    def update_query(self, place_query, request):
        db=self.db
        place_query.update(request.model_dump(), synchronize_session=False)
        db.commit()
