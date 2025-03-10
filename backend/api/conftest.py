import pytest
from rest_framework.test import APIClient
from api.models import User, Post, sessionmaker, engine
import datetime
import time

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def db_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.query(Post).delete()
    session.query(User).delete()
    session.commit()
    session.close()

@pytest.fixture
def sample_user(db_session):
    user = User(username="testuser", email="test@example.com", password="password")
    db_session.add(user)
    db_session.commit()
    print(f"Sample user created: {user.username}")
    return user

@pytest.fixture
def sample_post(db_session, sample_user):
    post = Post(title="Test Post", content="Test Content", author=sample_user)
    db_session.add(post)
    db_session.commit()
    return post

@pytest.fixture
def sample_post_dal(db_session, sample_user):
    post = Post(title="Sample Post", content="Sample Content", author=sample_user)
    db_session.add(post)
    db_session.commit()
    return post