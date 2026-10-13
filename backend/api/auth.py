from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from backend.schemas.auth import UserCreate, UserResponse
from backend.services.auth import register_user
from backend.database.dependencies import get_db

router = APIRouter()

@router.post('/register', response_model=UserResponse, status_code=201)
def register(user: UserCreate,
    db: Session = Depends(get_db)
):
    registered_user = register_user(db, user.name, user.email, user.password)
    return registered_user