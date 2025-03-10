from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Post, sessionmaker, engine
from .serializers import UserSerializer, PostSerializer
from .dal import UserDAL, PostDAL
import logging
from sqlalchemy.orm import joinedload
from django.core.cache import cache

# Configure logger for debugging
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling User API operations.
    Provides CRUD functionality for User model.
    """
    serializer_class = UserSerializer
    user_dal = UserDAL()

    def get_queryset(self):
        """Retrieve all users from the database."""
        Session = sessionmaker(bind=engine)
        with Session() as db_session:
            return db_session.query(User).all()

    def create(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Session = sessionmaker(bind=engine)
        with Session() as db_session:
            try:
                user = self.user_dal.create_user(serializer.validated_data, db_session)
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating user: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Post API operations.
    Provides CRUD functionality for Post model with caching for performance optimization.
    """
    serializer_class = PostSerializer
    post_dal = PostDAL()

    def get_queryset(self):
        """Retrieve all posts from cache or database if not cached."""
        cache_key = "all_posts"  # Unique cache key for posts
        cached_posts = cache.get(cache_key)

        if cached_posts:
            logger.info("Returning cached posts")
            return cached_posts

        logger.info("Fetching posts from database")
        Session = sessionmaker(bind=engine)
        with Session() as db_session:
            posts = db_session.query(Post).options(joinedload(Post.author)).all()
            cache.set(cache_key, posts, timeout=3600)  # Cache for 1 hour
            return posts

    def retrieve(self, request, pk=None, *args, **kwargs):
        """Retrieve a single post by ID."""
        Session = sessionmaker(bind=engine)
        with Session() as db_session:
            post = self.post_dal.get_post_by_id(pk, db_session)
            if not post:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(post)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new post and clear the cache to refresh data."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_data = serializer.validated_data
        post_data['author_id'] = serializer.validated_data.get('author_id')
        Session = sessionmaker(bind=engine)
        with Session() as db_session:
            try:
                post = self.post_dal.create_post(post_data, db_session)
                if not post:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                
                cache.delete("all_posts")  # Invalidate cache after creation
                return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating post: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        """Update an existing post and clear the cache."""
        Session = sessionmaker(bind=engine)
        with Session() as db_session:
            post = self.post_dal.get_post_by_id(pk, db_session)
            if not post:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(post, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            try:
                updated_post = self.post_dal.update_post(post, serializer.validated_data, db_session)
                cache.delete("all_posts")  # Invalidate cache after update
                return Response(PostSerializer(updated_post).data)
            except Exception as e:
                logger.error(f"Error updating post: {e}")
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, *args, **kwargs):
        """Delete a post and clear the cache."""
        Session = sessionmaker(bind=engine)
        with Session() as db_session:
            post = self.post_dal.get_post_by_id(pk, db_session)
            if not post:
                return Response(status=status.HTTP_404_NOT_FOUND)
            self.post_dal.delete_post(post, db_session)
            cache.delete("all_posts")  # Invalidate cache after deletion
            return Response(status=status.HTTP_204_NO_CONTENT)


class CachedUserViewSet(viewsets.ViewSet):
    """
    ViewSet for handling User API operations with caching.
    Retrieves a paginated list of users and stores results in cache for improved performance.
    """

    def list(self, request):
        """Retrieve a paginated list of users from cache or database."""
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        cache_key = f"users_page_{page}_per_page_{per_page}"
        cached_users = cache.get(cache_key)

        if not cached_users:
            user_dal = UserDAL()
            users = user_dal.get_all_users_paginated(page, per_page)
            serializer = UserSerializer(users, many=True)
            cache.set(cache_key, serializer.data, timeout=3600)  # Cache for 1 hour
            return Response(serializer.data)
        else:
            return Response(cached_users)
