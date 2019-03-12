from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import Http404
from user import models
from user import forms
from .querys import get_related_articles


def get_comments(article):
    comments = models.Comment.objects.filter(article__exact=article.id, reply_id__exact=False)
    replies = map(lambda x: (x, models.Comment.objects.filter(reply_id__exact=x.id)), comments)
    return list(replies)


def article(request, id):
    try:
        article = models.Article.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404
    article.views += 1
    article.save()
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    comments = get_comments(article)
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
