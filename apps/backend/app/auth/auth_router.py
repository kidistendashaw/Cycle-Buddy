from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.auth import hash_password, verify_password, create_access_token
from app.schemas import UserCreate, LoginRequest, AuthResponse, UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


# ── Register ─────────────────────
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user_data.password)
    new_user = models.User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ── Login ────────────────────────
@router.post("/login", response_model=AuthResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"user_id": user.id})

    return AuthResponse(
        access_token=token,
        user=user
    )
