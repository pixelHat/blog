from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from user import models
from user import forms
from .querys import get_popular_articles


def search_field(request, field, value):
    if field == 'category':
        articles = models.Article.objects.filter(category__id=value)\
                         .order_by('-published')
    elif field == 'tags':
        articles = models.Article.objects.filter(tags__id=value)\
                         .order_by('-published')
    else:
        raise Http404()
    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    context = {
        'articles': articles_page,
        'categories': categories,
        'tags': tags,
        'popular_articles': get_popular_articles(),
        'form': forms.NotifyForm(),
    }
    return render(request, 'user/index.html', context)


def search(request):
    title = request.GET.get('title')
    q1 = Q(title__contains=title)
    q2 = Q(text__contains=title)
    articles = models.Article.objects.filter(q1 | q2).order_by('-published')
    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    context = {
        'articles': articles_page,
        'categories': categories,
        'tags': tags,
        'popular_articles': get_popular_articles(),
        'form': forms.NotifyForm(),
    }
    return render(request, 'user/index.html', context)
