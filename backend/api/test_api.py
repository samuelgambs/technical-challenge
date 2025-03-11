import pytest
from api.models import User, Post, sessionmaker, engine
from unittest.mock import patch
from rest_framework import status
from api.serializers import UserSerializer, PostSerializer
from api.dal import UserDAL, PostDAL
import logging

# Configure logger for debugging
logger = logging.getLogger(__name__)


# 🧪 USER TESTS 🧪
@pytest.mark.django_db
def test_get_users(api_client, db_session, sample_user):
    """Test retrieving all users."""
    response = api_client.get('/api/v1/users/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['username'] == sample_user.username

@pytest.mark.django_db
def test_get_user(api_client, sample_user):
    """Test retrieving a single user by ID."""
    print(f"Testing user ID: {sample_user.id}")  # Debugging print
    response = api_client.get(f'/api/v1/users/{sample_user.id}/')
    assert response.status_code == 200  # Deve retornar 200 agora


@pytest.mark.django_db
def test_create_user(api_client, db_session):
    """Test creating a new user."""
    data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'password'}
    response = api_client.post('/api/v1/users/', data)
    assert response.status_code == 201
    assert response.data['username'] == 'newuser'

@pytest.mark.django_db
def test_update_user(api_client, db_session, sample_user):
    """Test updating an existing user."""
    db_session.refresh(sample_user)  # Garante que o usuário está atualizado
    data = {'username': 'updateduser', 'email': 'updateduser@example.com', 'password': 'newpassword'}
    response = api_client.put(f'/api/v1/users/{sample_user.id}/', data)
    assert response.status_code == 200
    assert response.data['username'] == 'updateduser'

@pytest.mark.django_db
def test_delete_user(api_client, db_session, sample_user):
    """Test deleting a user."""
    db_session.refresh(sample_user)  # Garante que o usuário realmente existe
    response = api_client.delete(f'/api/v1/users/{sample_user.id}/')
    assert response.status_code == 204

    # Verifica se o usuário foi realmente deletado
    response = api_client.get(f'/api/v1/users/{sample_user.id}/')
    assert response.status_code == 404


# 🧪 POST TESTS 🧪
@pytest.mark.django_db
def test_create_post(api_client, db_session, sample_user):
    """Test creating a new post."""
    data = {'title': 'New Post', 'content': 'Content of new post', 'author_id': sample_user.id}
    response = api_client.post('/api/v1/posts/', data)
    assert response.status_code == 201
    assert response.data['title'] == 'New Post'

@pytest.mark.django_db
def test_get_posts(api_client, db_session, sample_post):
    """Test retrieving all posts."""
    response = api_client.get('/api/v1/posts/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == sample_post.title

@pytest.mark.django_db
def test_get_post(api_client, db_session, sample_post):
    """Test retrieving a single post by ID."""
    response = api_client.get(f'/api/v1/posts/{sample_post.id}/')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_post(api_client, db_session, sample_post):
    """Test updating an existing post."""
    data = {'title': 'Updated Post', 'content': 'Updated content', 'author_id': sample_post.author.id}
    logger.debug(f"Sending data to update post: {data}")
    response = api_client.put(f'/api/v1/posts/{sample_post.id}/', data)
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response data: {response.data}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_post(api_client, db_session, sample_post):
    """Test deleting a post."""
    response = api_client.delete(f'/api/v1/posts/{sample_post.id}/')
    assert response.status_code == 204
    response = api_client.get(f'/api/v1/posts/{sample_post.id}/')
    assert response.status_code == 404


# 🧪 EXCEPTION HANDLING TESTS 🧪
@pytest.mark.django_db
def test_create_post_exception(api_client, db_session, sample_user):
    """Test exception handling when creating a post."""
    with patch('api.dal.PostDAL.create_post') as mock_create_post:
        mock_create_post.side_effect = Exception("Database error")
        data = {'title': 'New Post', 'content': 'Content of new post', 'author_id': sample_user.id}
        response = api_client.post('/api/v1/posts/', data)
    assert response.status_code == 500
    assert "Database error" in str(response.data)

@pytest.mark.django_db
def test_create_user_exception(api_client, db_session):
    """Test exception handling when creating a user."""
    with patch('api.dal.UserDAL.create_user') as mock_create_user:
        mock_create_user.side_effect = Exception("Database error")
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'password'}
        response = api_client.post('/api/v1/users/', data)
    assert response.status_code == 500
    assert "Database error" in str(response.data)


# 🧪 MODEL TESTS 🧪
@pytest.mark.django_db
def test_models(db_session, sample_user):
    """Test database model creation."""
    post = Post(title="test", content="test content", author=sample_user)
    db_session.add(post)
    db_session.commit()
    assert post.title == "test"
    assert post.author == sample_user


# 🧪 SERIALIZER TESTS 🧪
@pytest.mark.django_db
def test_serializers(sample_user, sample_post):
    """Test User and Post serializers."""
    user_serializer = UserSerializer(sample_user)
    post_serializer = PostSerializer(sample_post)
    assert user_serializer.data['username'] == sample_user.username
    assert post_serializer.data['title'] == sample_post.title



# 🧪 DAL TESTS 🧪
@pytest.mark.django_db
def test_dal(db_session, sample_user):
    """Test Data Access Layer (DAL) functionality."""
    user_dal = UserDAL()
    post_dal = PostDAL()

    # Criar post diretamente no teste
    post = Post(title="Sample Post", content="Sample Content", author=sample_user)
    db_session.add(post)
    db_session.commit()

    print(f"Generated Post ID: {post.id}")

    # 🟢 Testar busca de usuário
    user = user_dal.get_user_by_id(sample_user.id, db_session)
    retrieved_post = post_dal.get_post_by_id(post.id, db_session)
    assert user.username == sample_user.username
    assert retrieved_post.title == "Sample Post"

    # 🟢 Testar busca de usuário que não existe
    assert user_dal.get_user_by_id(9999, db_session) is None

    # 🟢 Testar atualização de usuário
    updated_user = user_dal.update_user(sample_user, {"username": "updateduser"}, db_session)
    assert updated_user.username == "updateduser"

    # 🟢 Testar deleção de usuário
    user_dal.delete_user(sample_user, db_session)
    assert user_dal.get_user_by_id(sample_user.id, db_session) is None

    # 🟢 Testar criação de usuário
    new_user_data = {"username": "test2", "email": "test2@example.com", "password": "password"}
    new_user = user_dal.create_user(new_user_data, db_session)
    assert new_user.username == "test2"

    # 🟢 Testar erro ao criar post sem autor válido
    invalid_post_data = {"title": "Orphan Post", "content": "No Author", "author_id": 9999}
    assert post_dal.create_post(invalid_post_data, db_session) is None

    # 🟢 Testar criação de post válido
    valid_post_data = {"title": "Valid Post", "content": "With Author", "author_id": new_user.id}
    valid_post = post_dal.create_post(valid_post_data, db_session)
    assert valid_post is not None
    assert valid_post.title == "Valid Post"

    # 🟢 Testar atualização de post
    updated_post = post_dal.update_post(valid_post, {"title": "Updated Post"}, db_session)
    assert updated_post.title == "Updated Post"

    # 🟢 Testar deleção de post
    post_dal.delete_post(valid_post, db_session)
    assert post_dal.get_post_by_id(valid_post.id, db_session) is None

    # 🟢 Testar paginação de posts (cria 10 posts)
    for i in range(10):
        db_session.add(Post(title=f"Post {i}", content="Content", author=new_user))
    db_session.commit()

    posts_page_1 = post_dal.get_all_posts_paginated(1, 5, db_session)
    posts_page_2 = post_dal.get_all_posts_paginated(2, 5, db_session)
    posts_page_3 = post_dal.get_all_posts_paginated(3, 5, db_session)

    assert len(posts_page_1) == 5
    assert len(posts_page_2) == 5
    assert len(posts_page_3) == 0
    
