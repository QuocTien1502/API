from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import DbPost
import datetime
from fastapi import HTTPException, status
from routers.schemas import UserAuth


def create(db: Session, request: PostBase):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.datetime.now(),
        user_id = request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session):
    return db.query(DbPost).all()

def delete(db: Session, id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    db.delete(post)
    db.commit()
    return {"message": f"Post with id {id} deleted successfully"}

def can_delete_post(post: DbPost, user: UserAuth):
    if user.role == "admin":
        return True
    if user.role == "user" and post.user_id == user.id:
        return True
    return False