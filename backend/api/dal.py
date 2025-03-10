from sqlalchemy.orm import Session, joinedload
from .models import User, Post

class UserDAL:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users_paginated(self, page: int, per_page: int):
        return (
            self.db.query(User)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    def create_user(self, user_data: dict):
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User, user_data: dict):
        for attr, value in user_data.items():
            setattr(user, attr, value)
        self.db.commit()
        return user

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()

class PostDAL:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_post_by_id(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_all_posts_paginated(self, page: int, per_page: int):
        return (
            self.db.query(Post)
            .options(joinedload(Post.author))
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    def create_post(self, post_data: dict):
        author_id = post_data.get('author_id')
        author = self.db.query(User).filter(User.id == author_id).first()
        if not author:
            return None  # Retorna None se o autor não for encontrado
        post = Post(**post_data)
        post.author = author
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update_post(self, post: Post, post_data: dict):
        for attr, value in post_data.items():
            setattr(post, attr, value)
        self.db.commit()
        return post

    def delete_post(self, post: Post):
        self.db.delete(post)
        self.db.commit()