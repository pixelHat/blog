from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import random


class User(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField()
    image = models.ImageField()

    def create_or_get(self, name, email):
        try:
            user = self.objects.get(email=email)
        except ObjectDoesNotExist:
            image = random.randint(1, 50)
            user = self.objects.create(name=name, email=email,
                                       image=f'avatars/{image}.png')
        return user

    def __str__(self):
        return f"{self.email}"


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"

    @property
    def num_articles(self):
        return self.category.count()


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    deleted = models.BooleanField(default=True)
    title = models.CharField(max_length=100, unique=True)
    published = models.DateTimeField()
    num_comments = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    text = models.TextField()
    image = models.ImageField()
    tags = models.ManyToManyField(Tag, blank=True,
                                  related_name="tags")
    category = models.ForeignKey(Category, blank=True, null=True,
                                 related_name="category",
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name="artifcle")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    comment = models.TextField()
    published = models.DateField(default="2019-02-28")


class Reply(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                   related_name="comment_parent")
    comment = models.TextField()


class Contact(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.title}"


class Notify(models.Model):
    """
    all users that want to be notify for latest articles.
    """
    email = models.EmailField(unique=True)
