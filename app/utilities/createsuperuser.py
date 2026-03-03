import os

import typer
# import database
from app.database.database import sessionLocal
from sqlalchemy.orm import Session
from app.database.models import User
from app.utilities.utils import get_hashed_password

from dotenv import load_dotenv
load_dotenv()

# creating instance of typer.
app = typer.Typer()

"""
here I not using the Depends because it is for fastapi, and so we are taking hte direct session.
"""

"""
NOTE: RUN COMMAND IS:
python -m app.utilities.createsuperuser
"""

@app.command()
def createsuperuser():
    # creating session here
    db= sessionLocal()
    first_name=os.environ.get("SUPERUSER_FIRST_NAME")
    last_name=os.environ.get("SUPERUSER_LAST_NAME")
    email=os.environ.get("SUPERUSER_EMAIL")
    password=os.environ.get("SUPERUSER_PASSWORD")

    is_superuser_exists = db.query(User).filter(User.email==email).first()
    if is_superuser_exists:
        print('superuser already exists')

    else:
        superuser = User(first_name=first_name,last_name=last_name,email=email,password=get_hashed_password(password),is_superuser=True, is_staff=True)
        db.add(superuser)
        db.commit()
        db.close()
        print('superuser created successfully')


if __name__ == "__main__":
    app()