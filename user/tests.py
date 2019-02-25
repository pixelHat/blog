from django.test import Client, TestCase
from django.contrib.auth.models import User
from unittest import mock
from django.core.files import File
from . import models
import tempfile


class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='user')

    def test_delete_article(self):
        pass

    def test_create_user(self):
        pass

    def test_try_create_existed_user(self):
        pass

    def test_get_user(self):
        pass


class ViewsTest(TestCase):
    """
    >>> test aside menu (tags and categories)
    """

    def setUp(self):
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        article1 = {
            'title': 'post1',
            'published': '2018-01-05',
            'text': 'post1 text',
            'image': image
        }
        article2 = {
            'title': 'post2',
            'published': '2018-01-10',
            'text': 'post2 text',
            'image': image,
        }
        article3 = {
            'title': 'post3',
            'published': '2018-01-22',
            'text': 'post3 text',
            'image': image,
        }
        models.Article.objects.create(**article1)
        models.Article.objects.create(**article2)
        models.Article.objects.create(**article3)
        models.Tag.objects.create(name='tag1')
        models.Category.objects.create(name='category1')

    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles'].object_list), 3)
        self.assertEqual(len(response.context['popular_articles']), 3)
        self.aside(response)

    def aside(self, response):
        """
        checks if the aside menu is correct.
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tags']), 1)
        self.assertEqual(len(response.context['categories']), 1)
