from django.core.paginator import Paginator
from django.shortcuts import render
from user import models
from user import forms
from .querys import get_latest_articles, get_popular_articles


def index(request):
    articles = get_latest_articles()
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
        'form': forms.NotifyForm()
    }
    return render(request, 'user/index.html', context)
