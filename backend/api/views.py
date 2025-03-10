from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Post, session
from .serializers import UserSerializer, PostSerializer
from .dal import UserDAL, PostDAL

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        user_dal = UserDAL(session)
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        users = user_dal.get_all_users_paginated(page, per_page)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_dal = UserDAL(session)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = user_dal.create_user(serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user_dal = UserDAL(session)
        user = user_dal.get_user_by_id(pk)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        user_dal = UserDAL(session)
        user = user_dal.get_user_by_id(pk)
        if user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                user = user_dal.update_user(user, serializer.validated_data)
                return Response(UserSerializer(user).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        user_dal = UserDAL(session)
        user = user_dal.get_user_by_id(pk)
        if user:
            user_dal.delete_user(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        post_dal = PostDAL(session)
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', 10))
        posts = post_dal.get_all_posts_paginated(page, per_page)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        post_dal = PostDAL(session)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = post_dal.create_post(serializer.validated_data)
            if post:
                return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Usuario não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        post_dal = PostDAL(session)
        post = post_dal.get_post_by_id(pk)
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        post_dal = PostDAL(session)
        post = post_dal.get_post_by_id(pk)
        if post:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                post = post_dal.update_post(post, serializer.validated_data)
                return Response(PostSerializer(post).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        post_dal = PostDAL(session)
        post = post_dal.get_post_by_id(pk)
        if post:
            post_dal.delete_post(post)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class CachedUserViewSet(viewsets.ViewSet):
    def list(self, request):
        cached_users = cache.get("users")
        if not cached_users:
            user_dal = UserDAL(session)
            users = user_dal.get_all_users_paginated(1, 100) #Implemente a paginação
            serializer = UserSerializer(users, many=True)
            cache.set("users", serializer.data, timeout=3600)
            return Response(serializer.data)
        else:
            return Response(cached_users)