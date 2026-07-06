from fastapi import status, HTTPException, Depends, APIRouter, Response
# This is pydantic, that used for the data defining that we will recieve from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
# This is the pydantic validation model
# This is the pydantic response model
from app.routers.users.pydanticModels import LoginUser, UpdateUser, UserCreate, UserResponse
from app.utilities.oauth2 import get_current_user
from app.routers.users.db_ops import UsersDbOps
from app.routers.users.helper_function import (
    create_staff_user_response,
    delete_user_response,
    login_response,
    update_user_response,
)


router = APIRouter(
    prefix='/api',
    tags=['Users']
)


def db_ops_init(db: Session = Depends(get_db)):
    return UsersDbOps(db)


# This is login endpoint.
@router.post('/login')
def login(user_cred: LoginUser, db_ops: Session = Depends(db_ops_init)):
    return login_response(user_cred, db_ops)


@router.post( '/create/user', status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    role = current_user.role

    if role == 'admin':
        return create_staff_user_response(request, db_ops)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")

@router.put('/user/update/{id}')
def user_update(id: int, request: UpdateUser, db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    role = current_user.role

    if role == 'admin':
        return update_user_response(id, request, db_ops)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")


@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User is not authenticated')
    return current_user

# This is delete user endpoint
@router.delete("/user/delete/{id}")
def delete_user(id: int, db_ops: Session = Depends(db_ops_init), current_user = Depends(get_current_user)):
    # Checking the role of the user
    role = current_user.role
    if role == 'admin':
        return delete_user_response(id, db_ops)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized User")


@router.post('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response):
    # Instructs the browser to clear the cookie by setting it to expire in the past
    response.delete_cookie(
        key="access_token", 
        path="/", 
        samesite="lax" # Match the SameSite configuration used when setting the cookie
    )
    return {"message": "Logged out successfully"}