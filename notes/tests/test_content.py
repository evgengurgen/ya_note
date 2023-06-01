from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author
            )
        cls.reader = User.objects.create(username='Читатель простой')

    def test_note_is_in_list(self):
        url = reverse('notes:list')
        users_statuses = (
            (self.author, True),
            (self.reader, False),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            response = self.client.get(url)
            object_list = response.context['object_list']
            self.assertEqual((self.notes in object_list), status)

    def test_form_edit_delete_note(self):
        self.client.force_login(self.author)
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes.slug,))
        )
        for name, args in urls:
            url = reverse(name, args=args)
            response = self.client.get(url)
            self.assertIn('form', response.context)
