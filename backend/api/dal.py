# dal.py
from sqlalchemy.orm import Session, joinedload, sessionmaker
from .models import User, Post, engine

class UserDAL:
    def get_user_by_id(self, user_id: int, session: Session = None):
        if session:
            return session.query(User).filter(User.id == user_id).first()
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                return db_session.query(User).filter(User.id == user_id).first()
            finally:
                db_session.close()

    def get_all_users_paginated(self, page: int, per_page: int, session: Session = None):
        if session:
            return session.query(User).offset((page - 1) * per_page).limit(per_page).all()
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                return db_session.query(User).offset((page - 1) * per_page).limit(per_page).all()
            finally:
                db_session.close()

    def create_user(self, user_data: dict, session: Session = None):
        if session:
            user = User(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                user = User(**user_data)
                db_session.add(user)
                db_session.commit()
                db_session.refresh(user)
                return user
            finally:
                db_session.close()

    def update_user(self, user: User, user_data: dict, session: Session = None):
        if session:
            for attr, value in user_data.items():
                setattr(user, attr, value)
            session.commit()
            return user
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                db_session.commit()
                return user
            finally:
                db_session.close()

    def delete_user(self, user: User, session: Session = None):
        if session:
            session.delete(user)
            session.commit()
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                db_session.delete(user)
                db_session.commit()
            finally:
                db_session.close()

class PostDAL:
    def get_post_by_id(self, post_id, session: Session = None):
        if session:
            return session.query(Post).filter(Post.id == post_id).first()
        else:
            Session = sessionmaker(bind=engine)
            session = Session()
            try:
                return session.query(Post).filter(Post.id == post_id).first()
            except NoResultFound:
                return None
            finally:
                session.close()

    def get_all_posts_paginated(self, page: int, per_page: int, session: Session = None):
        if session:
            return session.query(Post).options(joinedload(Post.author)).offset((page - 1) * per_page).limit(per_page).all()
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                return db_session.query(Post).options(joinedload(Post.author)).offset((page - 1) * per_page).limit(per_page).all()
            finally:
                db_session.close()

    def create_post(self, post_data: dict, session: Session = None):
        if session:
            author_id = post_data.get('author_id')
            author = session.query(User).filter(User.id == author_id).first()
            if not author:
                return None
            post = Post(**post_data)
            post.author = author
            session.add(post)
            session.commit()
            session.refresh(post)
            return post
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                author_id = post_data.get('author_id')
                author = db_session.query(User).filter(User.id == author_id).first()
                if not author:
                    return None
                post = Post(**post_data)
                post.author = author
                db_session.add(post)
                db_session.commit()
                db_session.refresh(post)
                return post
            finally:
                db_session.close()

    def update_post(self, post: Post, post_data: dict, session: Session = None):
        if session:
            for attr, value in post_data.items():
                setattr(post, attr, value)
            session.commit()
            return post
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                for attr, value in post_data.items():
                    setattr(post, attr, value)
                db_session.commit()
                return post
            finally:
                db_session.close()

    def delete_post(self, post: Post, session: Session = None):
        if session:
            session.delete(post)
            session.commit()
        else:
            Session = sessionmaker(bind=engine)
            db_session = Session()
            try:
                db_session.delete(post)
                db_session.commit()
            finally:
                db_session.close()