from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import Http404
from user import models
from user import forms
from .querys import get_related_articles


def article(request, id):
    try:
        article = models.Article.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404
    article.views += 1
    article.save()
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    comments = models.Comment.objects.filter(article__exact=article.id)
    context = {
        'article': article,
        'categories': categories,
        'tags': tags,
        'related_articles': get_related_articles(article),
        'comments': comments,
        'form': forms.NotifyForm(),
        'form_comment': forms.CommentForm(initial={'article': article.id,
                                                   'reply': 0}),
    }
    return render(request, 'user/article.html', context)
