from app.routers.places.models import Place
from fastapi import status, HTTPException
from app.routers.votes_ratings_feedback.models import Ratings, Votes
from sqlalchemy import and_, or_, cast, String
from app.routers.votes_ratings_feedback.utilities.calc_avg_rating import calculate_average_rating_all_categories
from app.routers.votes_ratings_feedback.utilities.calc_votes import calculate_vote




# This is the function for all place response with vote and ratings.
def all_place_response(current_user, db, place=None):
    place = db.all_place_query()
    if current_user:
        user_id = current_user.id
        # This is for logged-in users

        # Now I am here creating a list of JSON/Dict structure so that I can store in the format that which place has vote
        place_with_vote = []
        # iterating the place and then extracting information.
        for place_row in place:
            place_id = place_row.id
            # Calculate votes for this place only.
            vote = db.all_vote_query(place_id)
            like, dislike = calculate_vote(vote)

            is_voted = db.is_voted_query(user_id, place_id)
            # using the function that will calculate the ratings.
            rating = db.all_rated_place_query(place_id)

            # It is return 9 things because of specific place, so we are using indexing
            rating_response = calculate_average_rating_all_categories(rating)

            average_rating = rating_response[1]
            total_user = rating_response[0]

            # checking is user is rated or not this place
            is_user_rated = db.is_user_rated_place_query(user_id, place_id)

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
            vote = db.all_vote_query(place_id)
            like, dislike = calculate_vote(vote)

            rating = db.all_rated_place_query(place_id)
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


def search_place_endpoint(current_user, db_ops, search):
    if search:
        search_query = search.split()
        place = db_ops.search_all_place()
        return all_place_response(current_user, db_ops, place)



def specific_place_response(db_ops, user_id, place_id):
    place = db_ops.place_query_with_id(place_id)    

    # Calculate votes for this place only.
    all_vote = db_ops.all_vote_query(place_id)
    like, dislike = calculate_vote(all_vote)

    # place is not available of that id then run this
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 

    # if place is available then run this
    is_user_voted = db_ops.is_voted_query(user_id, place_id)

    rating = db_ops.all_rated_place_query(place_id)

    # It is return 9 things because of specific place, so we are using indexing
    ratings = calculate_average_rating_all_categories(rating)

    is_user_rated = db_ops.is_user_rated_place_query(user_id, place_id)

    place_with_vote = {
        "place_name": place.place_name,
        "place_address": place.place_address,
        "about_place": place.about_place,
        "pincode": place.pincode,
        "created_at": place.created_at,
        "id": place.id,
        "voted": is_user_voted.vote if is_user_voted else None,
        "num_likes": like,
        "num_dislikes": dislike,

        "overall": ratings[1],
        "cleanliness": ratings[2],
        "safety": ratings[3],
        "crowd_behavior": ratings[4],
        "transport_access": ratings[5],
        "lightning": ratings[6],
        "facility_quality": ratings[7],
        "total_user_rated": ratings[0],
        "is_user_rated": bool(is_user_rated)
    }
    return place_with_vote



