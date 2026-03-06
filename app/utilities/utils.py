# NOTE: utils means the helper functions, that's why it's name is utils
from app.database.models import Ratings, Place, Votes
import bcrypt
from sqlalchemy import and_, or_, cast, String

def get_hashed_password(plain_password: str) -> str:
    password = bcrypt.hashpw(plain_password.encode("utf-8"),bcrypt.gensalt())
    return password.decode("utf-8")

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

# This is function is for the place file to calculate the number of likes and dislikes
def calculate_vote(vote):
    like = 0
    dislike = 0
    for all_row in vote:
        if all_row.vote is True:
            like = like+1
        elif all_row.vote is False:
            dislike = dislike+1

    # print(like, dislike)
    # This will be returned as tuples
    return like, dislike

# This is for calculating the overall all categories average ratings
"""
formula:
average_rating_of_each_categories = sum of all the ratings of the one categories/total user did this.

and for overall average.
overall_average_rating = all categories overall rating/number of categories
"""
def calculate_average_rating_all_categories(rating):

    if rating:
        total_user_rating = len(rating)
        # making the empty list of all the categories so that I can store the number all ratings
        overall = []
        cleanliness = []
        safety = []
        crowd_behavior = []
        transport_access = []
        lightning = []
        facility_quality = []
        for all_categories in rating:
            overall.append(all_categories.overall)
            cleanliness.append(all_categories.cleanliness)
            safety.append(all_categories.safety)
            crowd_behavior.append(all_categories.crowd_behavior)
            transport_access.append(all_categories.transport_access)
            lightning.append(all_categories.lightning)
            facility_quality.append(all_categories.facility_quality)

        # creating each categories variable for storing the sum of all ratings.
        each_overall_sum = 0
        each_cleanliness_sum = 0
        each_safety_sum = 0
        each_crowd_behavior_sum = 0
        each_transport_access_sum = 0
        each_lightning_sum = 0
        each_facility_quality_sum = 0


        # now I am calculating the average rating of the categories

        # calculating average for overall ratings
        for each_rating in overall:
            each_overall_sum += each_rating

        # calculating the average of overall rating
        average_overall_rating = each_overall_sum/total_user_rating

        # calculating average for cleanliness
        for each_rating in cleanliness:
            each_cleanliness_sum += each_rating

        # calculating the average of cleanliness rating
        average_cleanliness_rating = each_cleanliness_sum/total_user_rating

        # calculating average for safety
        for each_rating in safety:
            each_safety_sum += each_rating

        # calculating the average of safety
        average_safety_rating = each_safety_sum/total_user_rating

        # calculating the average for crowd_behavior
        for each_rating in crowd_behavior:
            each_crowd_behavior_sum += each_rating

        average_crowd_behavior = each_crowd_behavior_sum/total_user_rating

        # calculating the average of transport rating
        for each_rating in transport_access:
            each_transport_access_sum += each_rating

        average_transport_access = each_transport_access_sum/total_user_rating

        # calculating the average of lightning rating
        for each_rating in lightning:
            each_lightning_sum += each_rating

        average_lightning = each_lightning_sum/total_user_rating

        for each_rating in facility_quality:
            each_facility_quality_sum += each_rating

        average_facility_quality = each_facility_quality_sum/total_user_rating

        # calculating the average of all categories


        # print(overall_average_rating)
        return total_user_rating, average_overall_rating, average_cleanliness_rating, average_safety_rating,average_crowd_behavior,average_transport_access, average_lightning, average_facility_quality

    else:
        return 0, 0, 0, 0, 0, 0, 0, 0

# This is the function for all place response with vote and ratings.
def all_place_response(current_user, db, search = None):

    """
    For searching pincode, I am using cast, that will convert pincode into string.

    """
    if search:
        search_query = search.split()
        place = []
        for all_query in search_query:
            search_pattern = f"%{all_query}%"
            place_search = db.query(Place).filter(or_(Place.place_name.ilike(search_pattern), (Place.about_place.ilike(search_pattern)), (Place.place_address.ilike(search_pattern)), (cast(Place.pincode, String).ilike(search_pattern)) )).limit(20).all()

            place.extend(place_search)


    #     here limit is used, so that only 20 place should return.
    else:
        place = db.query(Place).all()

    if current_user:
        user_id = current_user.id
        # This is for logged-in users

        # Now I am here creating a list of JSON/Dict structure so that I can store in the format that which place has vote
        place_with_vote = []
        # iterating the place and then extracting information.
        for place_row in place:
            place_id = place_row.id
            # Calculate votes for this place only.
            like, dislike = calculate_vote(
                db.query(Votes).filter(Votes.place_id == place_id).all()
            )
            is_voted = db.query(Votes).filter(and_(Votes.user_id==user_id, Votes.place_id==place_id)).first()
            # using the function that will calculate the ratings.
            rating = db.query(Ratings).filter(Ratings.place_id == place_id).all()

            # It is return 9 things because of specific place, so we are using indexing
            rating_response = calculate_average_rating_all_categories(rating)

            average_rating = rating_response[1]
            total_user = rating_response[0]

            # checking is user is rated or not this place
            is_user_rated = db.query(Ratings).filter(and_(Ratings.user_id==user_id, Ratings.place_id==place_id)).first()
            place_with_vote.append({
                "place_name": place_row.place_name,
                "place_address": place_row.place_address,
                "about_place": place_row.about_place,
                "pincode": place_row.pincode,
                "created_at": place_row.created_at,
                "id": place_id,
                "voted": is_voted.vote if is_voted else None,
                "num_likes": like,
                "num_dislikes": dislike,
                "overall": average_rating,
                "total_user_rated": total_user,
                "is_user_rated": bool(is_user_rated)
            })


        return place_with_vote
    else:
        # if not current user
        """
        problem will be:
        In pydantic, num of like and dislike and overall rating is also, so I need to create the new rows.
        """
        # creating a list
        # this place contains all the data
        all_places = []

        # so I am creating a list.
        for place_row in place:
            place_id = place_row.id
            # Calculate votes for this place only.
            like, dislike = calculate_vote(
                db.query(Votes).filter(Votes.place_id == place_id).all()
            )
            rating = db.query(Ratings).filter(Ratings.place_id == place_id).all()
            # using the function that will calculate the ratings.
            rating_response = calculate_average_rating_all_categories(rating)
            average_rating = rating_response[1]
            total_user = rating_response[0]
            # if vote is given by the user
            all_places.append({
                "place_name":place_row.place_name,
                "place_address":place_row.place_address,
                "about_place":place_row.about_place,
                "pincode":place_row.pincode,
                "created_at":place_row.created_at,
                "id": place_id,
                "num_likes":like,
                "num_dislikes":dislike,
                "overall": average_rating,
                "total_user_rated": total_user
            })
        return all_places
