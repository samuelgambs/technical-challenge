from rest_framework import serializers
from .models import User, Post, sessionmaker, engine
from sqlalchemy.orm import Session, joinedload
import logging

# Configure logger for debugging
logger = logging.getLogger(__name__)


class UserSerializer(serializers.Serializer):
    """
    Serializer for the User model.
    Handles serialization and deserialization of User objects.
    """
    id = serializers.IntegerField(read_only=True)  # Read-only, auto-generated ID
    username = serializers.CharField()  # Required username
    email = serializers.EmailField()  # Required email (must be unique)
    password = serializers.CharField(write_only=True)  # Write-only for security
    created_at = serializers.DateTimeField(read_only=True)  # Read-only timestamp

    def create(self, validated_data):
        """
        Create a new User instance.
        This method initializes a User object but does not commit it to the database.
        """
        return User(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing User instance.
        Loops through validated data and updates attributes dynamically.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance


class PostSerializer(serializers.Serializer):
    """
    Serializer for the Post model.
    Handles serialization and deserialization of Post objects.
    """
    id = serializers.IntegerField(read_only=True)  # Read-only, auto-generated ID
    title = serializers.CharField()  # Required post title
    content = serializers.CharField()  # Required post content
    created_at = serializers.DateTimeField(read_only=True)  # Read-only timestamp

    # SerializerMethodField allows us to customize how a field is retrieved
    author = serializers.SerializerMethodField()
    author_id = serializers.IntegerField(write_only=True)  # Only required on input

    def get_author(self, obj):
        """
        Retrieve the author's details using the UserSerializer.
        Ensures that the full author data is returned when fetching a post.
        """
        if obj.author:
            return UserSerializer(obj.author).data
        return None

    def create(self, validated_data):
        """
        Create a new Post instance.
        This method initializes a Post object but does not commit it to the database.
        """
        return Post(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing Post instance.
        Loops through validated data and updates attributes dynamically.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance

    def validate_author_id(self, value):
        """
        Custom validation for author_id.
        Ensures that the provided author_id corresponds to an existing User in the database.
        """
        logger.debug(f"Validating author_id: {value}")
        Session = sessionmaker(bind=engine)
        db_session = Session()

        try:
            author = db_session.query(User).filter(User.id == value).first()
            if author is None:
                logger.warning(f"Author with id {value} does not exist.")
                raise serializers.ValidationError("Author does not exist.")
            logger.debug(f"Author with id {value} found.")
            return value
        finally:
            db_session.close()
