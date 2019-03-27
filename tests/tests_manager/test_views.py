from django.contrib.auth.models import User
from django.test import Client, TestCase
import tempfile
from user import models

IMAGE = tempfile.NamedTemporaryFile(suffix=".jpg").name


class CommentViews(TestCase):
    def setUp(self):
        User.objects.create_user(username='root', password='pass')
        self.client = Client()
        self.client.login(username='root', password='pass')

        article_input = {
            'title': 'article 1',
            'text': 'text from article 1',
            'image': IMAGE,
        }
        article = models.Article.objects.create(**article_input)
        user = models.User.objects.create(name='user1',
                                          email='user1@email.com',
                                          image=IMAGE)
        comment_input = {
            'article': article,
            'user': user,
            'comment': 'comment 1',
        }
        models.Comment.objects.create(**comment_input)

    def test_show_comment(self):
        response = self.client.get('/manager/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['new_comments']), 1)
        self.assertEqual(len(response.context['waiting_comments']), 0)

    def test_read_comment(self):
        response = self.client.get('/manager/comments/read/', {'id': 1})
        comment = models.Comment.objects.get(pk=1)
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertTrue(comment.was_read_by_manager)

    def test_read_invalid_comment(self):
        response = self.client.get('/manager/comments/read/', {'id': 10})
        self.assertJSONEqual(response.content, {'ok': False})

    def test_delete_comment(self):
        response = self.client.get('/manager/comments/delete/', {'id': 1})
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertEqual(models.Comment.objects.count(), 0)

    def test_delete_invalid_comment(self):
        response = self.client.get('/manager/comments/delete/', {'id': 10})
        self.assertJSONEqual(response.content, {'ok': False})
        self.assertEqual(models.Comment.objects.count(), 1)

    def test_add_to_waiting_list(self):
        response = self.client.get('/manager/comments/add/waitList/', {'id': 1})
        comment = models.Comment.objects.get(pk=1)
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertTrue(comment.is_on_the_waiting_list)

    def test_add_invalid_comment_to_waiting_list(self):
        response = self.client.get('/manager/comments/add/waitList/', {'id': 10})
        self.assertJSONEqual(response.content, {'ok': False})
