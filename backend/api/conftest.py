import pytest
from rest_framework.test import APIClient
from api.models import User, Post, sessionmaker, engine
import datetime

@pytest.fixture
def api_client():
    """
    Returns an instance of APIClient to interact with the Django REST API.
    """
    return APIClient()

@pytest.fixture
def db_session():
    """
    Creates a new database session for testing.
    Ensures the session is rolled back and tables are cleaned up after each test.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # Provide session to the test
    session.rollback()  # Rollback any uncommitted changes
    session.query(Post).delete()  # Clean up posts
    session.query(User).delete()  # Clean up users
    session.commit()  # Ensure changes are persisted
    session.close()  # Close session

@pytest.fixture
def sample_user(db_session):
    user = User(username="testuser", email="test@example.com", password="password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # Ensures that the user has been saved in the database
    print(f"Sample user created: {user.id} - {user.username}")  # Debugging
    return user

@pytest.fixture
def sample_post(db_session, sample_user):
    """
    Creates and returns a sample post associated with the sample user.
    """
    post = Post(title="Test Post", content="Test Content", author=sample_user)
    db_session.add(post)
    db_session.commit()
    return post

@pytest.fixture
def sample_post_dal(db_session, sample_user):
    """
    Creates and returns another sample post (used for Data Access Layer tests).
    """
    post = Post(title="Sample Post", content="Sample Content", author=sample_user)
    db_session.add(post)
    db_session.commit()
    return post
