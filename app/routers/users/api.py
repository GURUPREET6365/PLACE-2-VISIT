from fastapi import status, HTTPException, Depends, APIRouter
# This is pydantic, that used for the data defining that we will recieve from the client.
from sqlalchemy.orm import Session
# Creating the table that we created in model.py
from app.database.database import get_db
# This is the pydantic validation model
# This is the pydantic response model
from app.routers.users.pydanticModels import LoginUser, UpdateUser, UserCreate, UserResponse
from app.database.models import User
# password hashing.
from app.utilities.utils import check_password, get_hashed_password
from app.utilities.oauth2 import create_access_token, get_current_user


router = APIRouter(
    prefix='/api',
    tags=['Users']
)


# This is login endpoint.
@router.post('/login')
def login(user_cred: LoginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_cred.email).first()

    # Verifying that is user exists or not, if exists then login and if not then send response that user is not registered.
    if not user:
        # print('user is not known')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    # print('matching password')
    if user.role == 'staff' or user.role == 'admin':

        is_match_pwd = check_password(user_cred.password, str(user.password))

        # Checking that the password matches or not.
        if not is_match_pwd:
            # print('password did not match')
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

        # if password matches then it will create the jwt token.
        access_token = create_access_token(data={'user_id': user.id, 'email': user.email})
        return {"token":access_token}

#     if login user is not the staff or admin then it will not log into
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorized User')


@router.post( '/create/user', status_code=status.HTTP_201_CREATED)
def create_user(request:UserCreate ,db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role

    if role == 'admin':
        if db.query(User).filter(User.email == request.email).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Email already exists")

        hashed_password = get_hashed_password(request.password)

        new_user = User(
            email=request.email,
            password=hashed_password,
            first_name=request.first_name,
            last_name=request.last_name,
            role='staff'
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message":"User created successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")

@router.put('/user/update/{id}')
def user_update(id:int, request: UpdateUser, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    role = current_user.role

    user_query = db.query(User).filter(User.id == id)
    is_user_exist = user_query.first()
    if role == 'admin':
        # if user not exists
        if not is_user_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The place of the id:{id} is not found.')


        user_query.update(request.model_dump(), synchronize_session=False)
        db.commit()
        return {"message":"user has been updated successfully"}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")


@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User is not authenticated')
    return current_user

# This is delete user endpoint
@router.delete("/user/delete/{id}")
def delete_user(id:int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Checking the role of the user
    role = current_user.role
    if role == 'admin':
        user = db.query(User).filter(User.id == id).first()
        if user:
            db.delete(user)
            db.commit()
            return {"message":"user deleted successfully"}

        # if user is not exists then
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="User Not Found")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized User")
