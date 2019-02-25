from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from . import models


def index(request):
    articles = models.Article.objects.all()
    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    popular_articles = models.Article.objects.order_by('num_comments')[:3]
    context = {
        'articles': articles_page,
        'categories': categories,
        'tags': tags,
        'popular_articles': popular_articles,
    }
    return render(request, 'user/index.html', context)


def article(request, id):
    try:
        article = models.Article.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    comments = models.Comment.objects.filter(article__exact=article.id)
    related_articles = models.Article.objects\
                                     .filter(category__exact=article.category)\
                                     .exclude(id__exact=article.id)
    context = {
        'article': article,
        'categories': categories,
        'tags': tags,
        'related_articles': related_articles,
        'comments': comments,
    }
    return render(request, 'user/article.html', context)
