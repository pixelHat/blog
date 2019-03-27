from django.utils import timezone
from django.test import Client, TestCase
import tempfile
from unittest import skip
from user import models

IMAGE = tempfile.NamedTemporaryFile(suffix=".jpg").name


from user.views.comment import get_comments
class CommentTest(TestCase):
    from user import forms

    def setUp(self):
        article_input = {
            'title': 'article 1',
            'published': timezone.now(),
            'text': 'body text of the article 1',
            'image': IMAGE,
        }
        user1_input = {
            'name': 'user1',
            'email': 'user1@email.com',
            'image': IMAGE,
        }
        self.article = models.Article.objects.create(**article_input)
        self.user = models.User.objects.create(**user1_input)

    def test_create_comment_for_existent_user(self):
        """
        should make a comment for a existent user.
        """
        client = Client()
        data = {'name': 'user1', 'article': 1, 'reply': 0,
                'email': 'user1@email.com', 'message': 'comment user 1'
                }
        response = client.post('/comment/', data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertEqual(len(models.User.objects.all()), 1)

    def test_create_comment_for_new_user(self):
        """
        should create a new user and after that make a new comment to his.
        """
        comment_input = {
            'article': models.Article.objects.get(pk=1),
            'user': models.User.objects.get(pk=1),
            'comment': 'comment form user 1',
        }
        models.Comment.objects.create(**comment_input)
        client = Client()
        response = client.post('/comment/', {'reply': 0, 'name': 'user2',
                                             'article': 1,
                                             'email': 'user2@email.com',
                                             'message': 'comment user 2'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertEqual(len(models.Comment.objects.all()), 2)
        self.assertEqual(len(models.User.objects.all()), 2)

    def test_comment_form(self):
        form_input = {
            'article': 1,
            'name': 'user',
            'email': 'user@email.com',
            'message': 'comment form user 1',
        }
        form = self.forms.CommentForm(data=form_input)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_article_field(self):
        form_input = {
            'article': models.Article.objects.count() + 1,
            'name': 'user',
            'email': 'user@email.com',
            'message': 'comment form user 1',
        }
        form = self.forms.CommentForm(data=form_input)
        self.assertFalse(form.is_valid())

    def test_get_comments(self):
        c1 = models.Comment.objects.create(article=self.article, user=self.user)
        c2 = models.Comment.objects.create(article=self.article, user=self.user)
        c3 = models.Comment.objects.create(article=self.article, user=self.user)
        expected = [c1, c2, c3]
        result = get_comments(self.article)
        self.assertEqual(expected, list(result))


class SearchTest(TestCase):
    def setUp(self):
        category1 = models.Category.objects.create(name='category 1')
        category2 = models.Category.objects.create(name='category 2')
        tag1 = models.Tag.objects.create(name='tag 1')
        articles = ({'title': 'article 1', 'published': timezone.now(),
                     'text': 'body text of the article 1', 'image': IMAGE,
                     'category': category1,
                     },
                    {
                    'title': 'article 2', 'published': timezone.now(),
                    'text': 'body text of the article 2', 'image': IMAGE,
                    'category': category1,
                    },
                    {
                    'title': 'article 3', 'published': timezone.now(),
                    'text': 'body text of the article 3', 'image': IMAGE,
                    'category': category2,
                    },
                    {
                    'title': 'article 4', 'published': timezone.now(),
                    'text': 'body text of the article 4', 'image': IMAGE,
                    })
        for article in articles:
            article = models.Article.objects.create(**article)
            article.tags.add(tag1)

    def test_search_text(self):
        client = Client()
        response = client.get('/search/', {'title': 'article'})
        self.assertEqual(len(response.context['articles']), 4)

    def test_search_category(self):
        client = Client()
        response = client.get('/search/category&1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 2)

    @skip('this need to be implemented')
    def test_search_category_does_not_exist(self):
        client = Client()
        response = client.get('/search/category&300')
        self.assertEqual(response.status_code, 404)

    def test_search_tag(self):
        client = Client()
        response = client.get('/search/tags&1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 4)

    def test_search_for_a_field_does_not_exist(self):
        client = Client()
        response = client.get('/search/doesNotExist&1')
        self.assertEqual(response.status_code, 404)


class RegisterEmailTest(TestCase):
    pass


class QueryArticles(TestCase):
    from user.views import querys

    def setUp(self):
        category1 = models.Category.objects.create(name='category 1')
        articles = ({'title': 'article 1', 'published': '2018-01-01',
                     'text': 'body text of the article 1', 'image': IMAGE,
                     'category': category1,
                     },
                    {
                    'title': 'article 2', 'published': '2018-01-02',
                    'text': 'body text of the article 2', 'image': IMAGE,
                    'category': category1,
                    },
                    {
                    'title': 'article 3', 'published': '2018-01-03',
                    'text': 'body text of the article 3', 'image': IMAGE,
                    'category': category1,
                    },
                    {
                    'title': 'article 4', 'published': '2018-01-04',
                    'text': 'body text of the article 4', 'image': IMAGE,
                    },
                    {
                    'title': 'article 5', 'published': '2018-01-05',
                    'text': 'body text of the article 5', 'image': IMAGE,
                    },
                    {
                    'title': 'article 6', 'published': '2018-01-06',
                    'text': 'body text of the article 6', 'image': IMAGE,
                    },
                    {
                    'title': 'article 7', 'published': '2018-01-07',
                    'text': 'body text of the article 7', 'image': IMAGE,
                    })
        for article in articles:
            article = models.Article.objects.create(**article)

    def test_latest_articles(self):
        pks = [i for i in range(7, 1, -1)]
        latest_articles = map(lambda x: models.Article.objects.get(pk=x), pks)
        response = self.querys.get_latest_articles()
        for (e1, e2) in zip(response, latest_articles):
            self.assertEqual(e1, e2)

    def test_related_articles(self):
        article = models.Article.objects.get(pk=1)
        q1 = models.Article.objects.filter(pk=2)
        q2 = models.Article.objects.filter(pk=3)
        related_articles = q1.union(q2)
        response = self.querys.get_related_articles(article)
        for (e1, e2) in zip(response, related_articles):
            self.assertEqual(e1, e2)

    def test_popular_articles(self):
        popular_articles = [models.Article.objects.get(pk=2),
                            models.Article.objects.get(pk=3),
                            models.Article.objects.get(pk=4)
                            ]
        for i, article in enumerate(popular_articles, 1):
            article.views = i*10
            article.save()
        response = self.querys.get_popular_articles()
        for (e1, e2) in zip(response, popular_articles[::-1]):
            self.assertEqual(e1, e2)

    @skip('how to test this?')
    def test_aside(self):
        pass


class ViewsTest(TestCase):
    def setUp(self):
        category1 = models.Category.objects.create(name='category 1')
        article_input1 = {'title': 'article 1', 'published': '2018-01-01',
                          'text': 'body text of the article 1', 'image': IMAGE,
                          'category': category1,
                          }
        article_input2 = {'title': 'article 2', 'published': '2018-01-02',
                          'text': 'body text of the article 2', 'image': IMAGE,
                          'category': category1,
                          }
        models.Article.objects.create(**article_input1)
        models.Article.objects.create(**article_input2)

    def test_home(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 2)
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(len(response.context['tags']), 0)
        self.assertNotEqual(len(response.context['popular_articles']), 0)

    def test_article(self):
        client = Client()
        response = client.get('/article/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(len(response.context['tags']), 0)
        self.assertEqual(len(response.context['comments']), 0)
