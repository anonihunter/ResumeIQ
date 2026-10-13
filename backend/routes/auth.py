from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from backend.database.dependencies import get_db
from backend.core.security import create_jwt_access_token
from backend.services.auth import register_user, login_user
from backend.dependencies.auth import get_current_user
from backend.schemas.auth import UserCreate, UserResponse, LoginRequest, TokenResponse

auth_router = APIRouter()

@auth_router.post(
    '/auth/register',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = register_user(db, user.name, user.email, user.password)
        return created_user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

@auth_router.post(
    '/auth/login',
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)

def user_login(user: LoginRequest, db: Session = Depends(get_db)):
    try:
        authenticated_user = login_user(db, user.email, user.password)
        access_token = create_jwt_access_token(
            data = {'sub': str(authenticated_user.id)}
        )
        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }
    

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Credentials'

        )


@auth_router.get(
    '/auth/me',
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def read_current_user(
    current_user = Depends(get_current_user)
):
    return current_user
