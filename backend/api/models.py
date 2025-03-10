from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base  # Using declarative base
from sqlalchemy.orm import sessionmaker, relationship
from django.conf import settings

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Fetch database configuration from Django settings
db_config = settings.DATABASES['default']
url = f"postgresql://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"

# Create database engine
engine = create_engine(url)

# Create session factory bound to the engine
Session = sessionmaker(bind=engine)


class User(Base):
    """User model representing registered users in the system."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)  # Unique username
    email = Column(String, unique=True, nullable=False)  # Unique email
    password = Column(String, nullable=False)  # Hashed password (should be stored securely)
    created_at = Column(DateTime, default=func.now())  # Timestamp for account creation

    # Relationship with posts (One-to-Many)
    posts = relationship("Post", back_populates="author", cascade='all, delete-orphan')

    def __repr__(self):
        """String representation of the User object."""
        return f"<User(username='{self.username}', email='{self.email}')>"


class Post(Base):
    """Post model representing user-generated posts."""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Post title
    content = Column(String, nullable=False)  # Post content
    created_at = Column(DateTime, default=func.now())  # Timestamp for post creation

    # Foreign key linking the post to the author (User)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="posts")  # Relationship with User

    def __repr__(self):
        """String representation of the Post object."""
        return f"<Post(title='{self.title}', author_id='{self.author_id}')>"


# Create tables in the database if they don't exist
Base.metadata.create_all(engine)
