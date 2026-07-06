from fastapi import HTTPException, status


def add_vote_response(place_id, request, db_ops, current_user):
    user_id = current_user.id

    place = db_ops.place_query_with_id(place_id)
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with id {place_id} not found"
        )

    vote = db_ops.user_vote_query(user_id, place_id)
    if vote is None:
        db_ops.create_vote(user_id, place_id, request.vote)
    else:
        db_ops.update_vote(vote, request.vote)

    return {"success": True}


def place_rating_response(place_id, request, db_ops, current_user):
    user_id = current_user.id
    ratings_query = db_ops.user_rating_query(user_id, place_id)
    ratings = ratings_query.first()

    request.user_id = user_id
    request.place_id = place_id

    if ratings:
        db_ops.update_rating(ratings_query, request)
        return {"message": "rating successfully updated"}

    db_ops.create_rating(request)
    return {"message": "rating successfully created"}


def feedback_response(request, db_ops):
    db_ops.create_feedback(request)
    return {"message": "feedback accepted successfully"}
