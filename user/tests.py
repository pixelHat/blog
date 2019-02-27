from django.test import Client, TestCase
from django.contrib.auth.models import User
import tempfile
from . import models


class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='user')

    def test_delete_article(self):
        pass

    def test_get_user(self):
        """
        should return a user with the same email or create a new.
        """
        user = {
            'name': 'user_name',
            'email': 'a@a.com',
        }
        u1 = models.User.create_or_get(models.User, **user)
        u2 = models.User.create_or_get(models.User, **user)
        self.assertEqual(u1.id, 1)
        self.assertEqual(u1, u2)

    def test_try_create_existed_user(self):
        pass


class ViewsTest(TestCase):
    def setUp(self):
        models.Tag.objects.create(name='tag1')
        cat = models.Category.objects.create(name='category1')
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        article1 = {
            'title': 'post1',
            'published': '2018-01-05',
            'text': 'post1 text',
            'image': image,
            'category': cat,
        }
        article2 = {
            'title': 'post2',
            'published': '2018-01-10',
            'text': 'post2 text',
            'image': image,
            'category': cat,
        }
        article3 = {
            'title': 'post3',
            'published': '2018-01-22',
            'text': 'post3 text',
            'image': image,
        }
        a1 = models.Article.objects.create(**article1)
        models.Article.objects.create(**article2)
        models.Article.objects.create(**article3)
        user = models.User.objects.create(name='user1', email='a@a.com',
                                          image=image)
        models.Comment.objects.create(article=a1, user=user, comment='good',
                                      published='2018-01-06')

    def test_index(self):
        """
        fail because the article.id == 1 is ignored.
        """
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles'].object_list), 3)
        self.assertEqual(len(response.context['popular_articles']), 3)
        self.aside(response)

    def test_article(self):
        """
        page for read the article.
        """
        client = Client()
        response = client.get('/article/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['comments']), 1)
        self.assertEqual(len(response.context['related_articles']), 1)
        self.aside(response)

    def aside(self, response):
        """
        checks if the aside menu is correct.
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tags']), 1)
        self.assertEqual(len(response.context['categories']), 1)
