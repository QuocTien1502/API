from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.datastructures import UploadFile
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from routers.schemas import PostBase, PostDisplay
from db.database import get_db
from fastapi.exceptions import HTTPException
from db import db_post, db_user
from typing import List
import random
import string
import shutil
from routers.schemas import UserAuth

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

image_url_types = ["absolute", "relative"]


@router.post("", response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
    return db_post.create(db, request)

@router.get("/all", response_model=List[PostDisplay])
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.get("/{username}", response_model=List[PostDisplay])
def get_posts_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(db_user.DbUser).filter(db_user.DbUser.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found"
        )

    user_posts = db.query(db_post.DbPost).filter(db_post.DbPost.user_id == user.id).all()
    if not user_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for user with username {username}"
        )

    return user_posts


@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}

@router.get("/delete/{id}")
# def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     return db_post.delete(db, id, current_user.id)
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    post = db.query(db_post.DbPost).filter(db_post.DbPost.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if not db_post.can_delete_post(post, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post"
        )

    return db_post.delete(db, id)

@router.delete("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    post = db.query(db_post.DbPost).filter(db_post.DbPost.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if not db_post.can_delete_post(post, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post"
        )

    return db_post.delete(db, id)

@router.put("/update-caption/{id}")
def update_caption(id: int, new_caption: str, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    post = db.query(db_post.DbPost).filter(db_post.DbPost.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if not db_post.can_delete_post(post, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post"
        )

    post.caption = new_caption
    db.commit()
    db.refresh(post)
    return {
        "message": "Caption updated successfully",
        "post_id": post.id,
        "new_caption": post.caption
    }

# @router.put("/update-caption/{id}")
# def update_caption(id: int, request: dict, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     post = db.query(db_post.DbPost).filter(db_post.DbPost.id == id).first()
#
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} not found"
#         )
#
#     if not db_post.can_delete_post(post, current_user):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You do not have permission to update this post"
#         )
#
#     new_caption = request.get("new_caption")
#     if not new_caption:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail="New caption cannot be empty"
#         )
#
#     post.caption = new_caption
#     db.commit()
#     db.refresh(post)
#     return {
#         "message": "Caption updated successfully",
#         "post_id": post.id,
#         "new_caption": post.caption
#     }