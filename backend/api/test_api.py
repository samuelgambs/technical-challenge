# api/test_api.py
import pytest
from rest_framework.test import APIClient
from .models import User, Post, session
from datetime import datetime
from sqlalchemy.orm import selectinload
from .serializers import UserSerializer, PostSerializer
from .dal import PostDAL


@pytest.fixture(autouse=True)
def clear_db():
    session.query(Post).delete()
    session.query(User).delete()
    session.commit()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_user():
    user = User(username="testuser", email="test@example.com", password="password", created_at=datetime.utcnow())
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def sample_post(sample_user):
    post = Post(title="Test Post", content="This is a test post.", author=sample_user, created_at=datetime.utcnow())
    session.add(post)
    session.commit()
    return post

@pytest.mark.django_db
def test_get_users(api_client, sample_user):
    response = api_client.get('/api/users/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['username'] == "testuser"
    assert response.data[0]['email'] == "test@example.com"

@pytest.mark.django_db
def test_get_posts(api_client, sample_post):
    response = api_client.get('/api/posts/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Test Post"
    assert response.data[0]['content'] == "This is a test post."
    assert response.data[0]['author']['username'] == "testuser"

@pytest.mark.django_db
def test_create_user(api_client):
    data = {"username": "newuser", "email": "newuser@example.com", "password": "password"}
    response = api_client.post('/api/users/', data)
    assert response.status_code == 201
    assert response.data['username'] == "newuser"
    assert response.data['email'] == "newuser@example.com"
    assert 'id' in response.data


@pytest.mark.django_db
def test_get_user(api_client, sample_user):
    response = api_client.get(f'/api/users/{sample_user.id}/')
    assert response.status_code == 200
    assert response.data['username'] == "testuser"
    assert response.data['email'] == "test@example.com"

@pytest.mark.django_db
def test_update_user(api_client, sample_user):
    data = {"username": "updateduser", "email": "updated@example.com", "password": "newpassword"}
    response = api_client.put(f'/api/users/{sample_user.id}/', data)
    assert response.status_code == 200
    assert response.data['username'] == "updateduser"
    assert response.data['email'] == "updated@example.com"

@pytest.mark.django_db
def test_delete_user(api_client, sample_user):
    response = api_client.delete(f'/api/users/{sample_user.id}/')
    assert response.status_code == 204
    response = api_client.get(f'/api/users/{sample_user.id}/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_create_post(api_client, sample_user):
    data = {"title": "New Post", "content": "New content.", "author_id": sample_user.id}
    response = api_client.post('/api/posts/', data)
    assert response.status_code == 201
    assert response.data['title'] == "New Post"
    assert response.data['content'] == "New content."
    assert response.data['author']['username'] == "testuser"

@pytest.mark.django_db
def test_get_post(api_client, sample_post):
    response = api_client.get(f'/api/posts/{sample_post.id}/')
    assert response.status_code == 200
    assert response.data['title'] == "Test Post"
    assert response.data['content'] == "This is a test post."
    assert response.data['author']['username'] == "testuser"

@pytest.mark.django_db
def test_update_post(api_client, sample_post):
    data = {"title": "Updated Post", "content": "Updated content.", "author_id": sample_post.author.id}
    response = api_client.put(f'/api/posts/{sample_post.id}/', data)
    assert response.status_code == 200
    assert response.data['title'] == "Updated Post"
    assert response.data['content'] == "Updated content."

@pytest.mark.django_db
def test_delete_post(api_client, sample_post):
    response = api_client.delete(f'/api/posts/{sample_post.id}/')
    assert response.status_code == 204
    response = api_client.get(f'/api/posts/{sample_post.id}/')
    assert response.status_code == 404

# api/test_api.py
# ...
@pytest.mark.django_db
def test_user_repr(sample_user):
    assert repr(sample_user) == f"<User(username='testuser', email='test@example.com')>"

@pytest.mark.django_db
def test_post_repr(sample_post):
    assert repr(sample_post) == f"<Post(title='Test Post', author_id='{sample_post.author_id}')>"

# api/test_api.py
# ...
@pytest.mark.django_db
def test_user_serializer_update(sample_user):
    serializer = UserSerializer(instance=sample_user, data={"username": "updated", "email": "updated@example.com"}, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_user = serializer.save()
    assert updated_user.username == "updated"
    assert updated_user.email == "updated@example.com"

@pytest.mark.django_db
def test_post_serializer_update(sample_post):
    serializer = PostSerializer(instance=sample_post, data={"title": "updated", "content": "updated content"}, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_post = serializer.save()
    assert updated_post.title == "updated"
    assert updated_post.content == "updated content"


@pytest.mark.django_db
def test_user_serializer_invalid_data():
    serializer = UserSerializer(data={"username": "", "email": "invalid"})
    assert not serializer.is_valid()
    assert 'username' in serializer.errors
    assert 'email' in serializer.errors


# api/test_api.py
# ...
@pytest.mark.django_db
def test_update_user_view(api_client, sample_user):
    data = {"username": "updated", "email": "updated@example.com", "password": "newpassword"}
    response = api_client.put(f'/api/users/{sample_user.id}/', data)
    assert response.status_code == 200
    assert response.data['username'] == "updated"

@pytest.mark.django_db
def test_retrieve_user_view(api_client, sample_user):
    response = api_client.get(f'/api/users/{sample_user.id}/')
    assert response.status_code == 200
    assert response.data['username'] == "testuser"

@pytest.mark.django_db
def test_delete_user_view(api_client, sample_user):
    response = api_client.delete(f'/api/users/{sample_user.id}/')
    assert response.status_code == 204

# Repita os testes para PostViewSet
@pytest.mark.django_db
def test_update_post_view(api_client, sample_post):
    data = {"title": "updated", "content": "updated content", "author_id": sample_post.author.id}
    response = api_client.put(f'/api/posts/{sample_post.id}/', data)
    assert response.status_code == 200
    assert response.data['title'] == "updated"

@pytest.mark.django_db
def test_retrieve_post_view(api_client, sample_post):
    response = api_client.get(f'/api/posts/{sample_post.id}/')
    assert response.status_code == 200
    assert response.data['title'] == "Test Post"

@pytest.mark.django_db
def test_delete_post_view(api_client, sample_post):
    response = api_client.delete(f'/api/posts/{sample_post.id}/')
    assert response.status_code == 204


@pytest.mark.django_db
def test_cached_user_view(api_client, sample_user):
    response = api_client.get('/api/cached_users/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['username'] == "testuser"


# api/test_api.py
# ...
@pytest.mark.django_db
def test_user_serializer_empty_data():
    serializer = UserSerializer(data={})
    assert not serializer.is_valid()
    assert 'username' in serializer.errors
    assert 'email' in serializer.errors
    assert 'password' in serializer.errors


# api/test_api.py
# ...
@pytest.mark.django_db
def test_get_user_not_found(api_client):
    response = api_client.get('/api/users/999/')
    assert response.status_code == 404


# @pytest.mark.django_db
# def test_get_users_pagination(api_client, transactional_db):
#     Session = sessionmaker(bind=engine)
#     db_session = Session()
#     # Crie 15 usuários para o teste
#     for i in range(15):
#         user = User(username=f"user{i}", email=f"user{i}@example.com", password="password")
#         db_session.add(user)
#     db_session.commit()

#     # Página 1, 10 usuários por página
#     response = api_client.get('/api/users/?page=1&per_page=10')
#     assert response.status_code == 200
#     assert len(response.data) == 10

#     # Página 2, 10 usuários por página
#     response = api_client.get('/api/users/?page=2&per_page=10')
#     assert response.status_code == 200
#     assert len(response.data) == 5

#     db_session.close()