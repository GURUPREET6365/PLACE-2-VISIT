from fastapi import HTTPException, status

from app.utilities.oauth2 import create_access_token
from app.utilities.utils import check_password, get_hashed_password


def login_response(user_cred, db_ops):
    user = db_ops.user_query_with_email(user_cred.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    if user.role == "staff" or user.role == "admin":
        is_match_pwd = check_password(user_cred.password, str(user.password))
        if not is_match_pwd:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Credentials"
            )

        access_token = create_access_token(data={"user_id": user.id, "email": user.email})
        return {"token": access_token}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized User"
    )


def create_staff_user_response(request, db_ops):
    if db_ops.user_query_with_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    hashed_password = get_hashed_password(request.password)
    db_ops.create_user(request, hashed_password)
    return {"message": "User created successfully"}


def update_user_response(user_id, request, db_ops):
    user_query = db_ops.user_update_query_with_id(user_id)
    is_user_exist = user_query.first()
    if not is_user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The place of the id:{user_id} is not found."
        )

    db_ops.update_user(user_query, request)
    return {"message": "user has been updated successfully"}


def delete_user_response(user_id, db_ops):
    user = db_ops.user_query_with_id(user_id)
    if user:
        db_ops.delete_user(user)
        return {"message": "user deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="User Not Found"
    )
