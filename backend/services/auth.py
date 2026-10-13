from sqlalchemy.orm import Session
from backend.models.user import User
from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError
from backend.core.security import hash_password, verify_password

def register_user(db: Session, name: str, email: str, password: str) -> User:
    # Generates: SELECT EXISTS (SELECT 1 FROM users WHERE users.email = :email)
    email_exists = db.scalar(
        select(exists().where(User.email == email)))

    if email_exists:
        raise ValueError(f"Registration failed: Email '{email}' is already registered.")

    new_user = User(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    try:
        # 5. Session lifecycle management
        db.add(new_user)
        db.commit()      # Flushes changes and commits the transaction
        db.refresh(new_user)  # Reloads attributes from the database (e.g., generated ID)
    
        # 6. Return the newly created User instance
        return new_user
    
    except IntegrityError as e:
        # Failsafe catch for race conditions where email was written between the check and commit
        db.rollback()
        raise ValueError("Registration failed: Database conflict encountered.") from e


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    return user

