from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import Http404
from user import forms, models
from .comment import get_comments
from .querys import get_related_articles


def article(request, id):
    try:
        article = models.Article.objects.get(pk=id)
        article.views += 1
        article.save()
    except ObjectDoesNotExist:
        raise Http404
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
        'form_comment': forms.CommentForm(initial={'article': article.id}),
    }
    return render(request, 'user/article.html', context)
