from fastapi import HTTPException, status


def require_role(current_user, allowed_roles):
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized User"
        )


def admin_place_response(db_ops, current_user):
    require_role(current_user, {"admin", "staff"})
    return db_ops.all_place_query()


def admin_search_place_response(search, db_ops, current_user):
    require_role(current_user, {"admin", "staff"})
    return db_ops.search_place(search.split())


def admin_user_response(db_ops, current_user):
    require_role(current_user, {"admin"})
    return db_ops.all_user_query()


def admin_search_user_response(search, db_ops, current_user):
    require_role(current_user, {"admin"})
    return db_ops.search_user(search.split())


def admin_vote_response(db_ops, current_user):
    require_role(current_user, {"admin"})
    return db_ops.all_votes_query()


def admin_rating_response(db_ops, current_user):
    require_role(current_user, {"admin"})
    return db_ops.all_ratings_query()


def admin_feedback_response(db_ops, current_user):
    require_role(current_user, {"admin", "staff"})
    return db_ops.all_feedback_query()
