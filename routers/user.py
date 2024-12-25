from fastapi import APIRouter, Depends,HTTPException, status
from routers.schemas import UserDisplay, UserBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user, models

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# @router.get("/{id}", response_model=UserDisplay)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.DbUser).filter(models.DbUser.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with ID {id} not found"
#         )
#     return user