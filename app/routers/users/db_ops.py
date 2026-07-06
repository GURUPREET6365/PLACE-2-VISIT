from app.routers.users.models import User


class UsersDbOps:
    def __init__(self, db):
        self.db = db

    def user_query_with_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def user_query_with_id(self, user_id):
        return self.db.query(User).filter(User.id == user_id).first()

    def user_update_query_with_id(self, user_id):
        return self.db.query(User).filter(User.id == user_id)

    def create_user(self, request, hashed_password, role="staff"):
        new_user = User(
            email=request.email,
            password=hashed_password,
            first_name=request.first_name,
            last_name=request.last_name,
            role=role
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_query, request):
        user_query.update(request.model_dump(), synchronize_session=False)
        self.db.commit()

    def delete_user(self, user):
        self.db.delete(user)
        self.db.commit()
