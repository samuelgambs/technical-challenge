# conftest.py
import pytest
from .models import sessionmaker, engine

@pytest.fixture
def db_session():
    Session = sessionmaker(bind=engine)
    db_session = Session()
    yield db_session
    db_session.close()