from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models

from app.database import get_db
from app.schema import UserCreate, UserOut
from app.utils import hash

router = APIRouter(tags=["users"])
# user routes


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password -> user.password
    hashed_password = hash(user.password)
    user.password = hashed_password  # replace with hashed password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{id}', response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id} does not exist.")
    return user
