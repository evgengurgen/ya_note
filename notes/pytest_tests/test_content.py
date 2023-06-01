import pytest
from django.urls import reverse


@pytest.mark.parametrize(
        'name, args',
        [
            ('notes:add', None),
            ('notes:edit', pytest.lazy_fixture('slug_for_args'))
        ]
)
def test_form_edit_delete_note(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context


@pytest.mark.parametrize(
        'user_client, in_list',
        [
            (pytest.lazy_fixture('admin_client'), False),
            (pytest.lazy_fixture('author_client'), True)
        ]
)
def test_note_is_in_list(user_client, in_list, note):
    url = reverse('notes:list')
    response = user_client.get(url)
    object_list = response.context['object_list']
    assert (note in object_list) is in_list
