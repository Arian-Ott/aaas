from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.models.user import User
from api.schemas.user import UserQuery, CreateUser


def get_user(db: Session, user: UserQuery, top_k: int = 1):
    """
    Filters the User table based on the non-None fields in the UserQuery.
    Raises ValueError if no matching user is found.
    """
    filters = []
    # Dump only the provided fields (non-None, non-unset)
    try:
        criteria = user.model_dump(exclude_none=True, exclude_unset=True)

        if "username" in criteria:
            filters.append(User.username == criteria.get("username"))
        if "email" in criteria:
            filters.append(User.email == criteria.get("email"))
        if "id" in criteria:
            filters.append(User.id == criteria.get("id"))

        if not filters:
            return None if top_k == 1 else []
    except AttributeError:
        pass # I know this is bad but I need it till i find a better way to handle this :)
    query = db.query(User).filter(or_(*filters))
    result = query.first() if top_k == 1 else query.all()
    if not result:
        return None
    return result


def create_user(db: Session, user: CreateUser):
    """
    Creates a new User instance using data from the CreateUser schema.
    Commits the new user to the database.
    """
    # Use model_dump to convert the pydantic model to a dict.
    new_user = User(**user.model_dump(exclude_none=True, exclude_unset=False))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    """
    Returns all users.
    """
    return db.query(User).all()


def delete_user(db: Session, user: UserQuery):
    """
    Deletes a user matching the query.
    """
    
    existing_user = get_user(db, user)
    
    db.delete(existing_user)
    db.commit()


def update_user(db: Session, user_query: UserQuery, new_user: CreateUser):
    """
    Updates an existing user.

    Instead of creating a new User instance, we update fields on the existing one.
    """
    # Retrieve the existing user based on the query.
    existing_user = get_user(db, user_query)

    # Get only the fields that are provided in new_user.
    updates = new_user.model_dump(exclude_none=True, exclude_unset=True)
    for key, value in updates.items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)
    return existing_user
