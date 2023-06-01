from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects
import pytest


@pytest.mark.parametrize(
    'name',
    ('notes:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:add', 'notes:list', 'notes:success')
)
def test_pages_availability_for_auth_user(author_client, name):
    url = reverse(name)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    [
        ('notes:list', None),
        ('notes:success', None),
        ('notes:add', None),
        ('notes:detail', pytest.lazy_fixture('slug_for_args')),
        ('notes:edit', pytest.lazy_fixture('slug_for_args')),
        ('notes:delete', pytest.lazy_fixture('slug_for_args'))
     ]
)
def test_redirect_anonymous(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
        'user_client, expected_status',
        [
            (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
        ]
)
@pytest.mark.parametrize(
    'name, args',
    [
        ('notes:detail', pytest.lazy_fixture('slug_for_args')),
        ('notes:edit', pytest.lazy_fixture('slug_for_args')),
        ('notes:delete', pytest.lazy_fixture('slug_for_args'))
     ]
)
def test_authors_pages(user_client, name, args, expected_status):
    url = reverse(name, args=args)
    response = user_client.get(url)
    assert response.status_code == expected_status
