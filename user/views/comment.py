from django.shortcuts import redirect
from django.urls import reverse
from user import models
from user import forms


def get_comments(article):
    comments = models.Comment.objects.filter(article__exact=article.id)
    return comments


def comment(request):
    form = forms.CommentForm(request.POST)
    if form.is_valid():
        article = models.Article.objects.get(pk=form.cleaned_data['article'])
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        user = models.User.create_or_get(models.User, name=name, email=email)
        models.Comment.objects.create(article=article, user=user, comment=message)
    return redirect(reverse('article', args=[article.id]))
