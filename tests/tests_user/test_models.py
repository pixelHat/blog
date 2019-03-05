from django.test import TestCase
from django.contrib.auth.models import User
from user import models


class ModelUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='user')

    def test_create_user(self):
        """
        should create a new user.
        """
        user_data = {
            'name': 'user_name',
            'email': 'a@a.com',
        }
        user = models.User.create_or_get(models.User, **user_data)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, user_data['name'])
        self.assertEqual(user.email, user_data['email'])

    def test_get_user(self):
        """
        should return a user with the same email.
        """
        user_data = {
            'name': 'user_name',
            'email': 'a@a.com',
        }
        user1 = models.User.create_or_get(models.User, **user_data)
        user2 = models.User.create_or_get(models.User, **user_data)
        self.assertEqual(user1.id, 1)
        self.assertEqual(user1, user2)
