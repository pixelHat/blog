from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render
from . import models
from . import forms
from django.http import JsonResponse


def index(request):
    articles = models.Article.objects.order_by('-published')\
                     .exclude(id__exact=1)
    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    popular_articles = models.Article.objects.exclude(id__exact=1)\
                             .order_by('-views')[:3]
    context = {
        'articles': articles_page,
        'categories': categories,
        'tags': tags,
        'popular_articles': popular_articles,
        'form': forms.NotifyForm()
    }
    return render(request, 'user/index.html', context)


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


def search_field(request, field, value):
    if field == 'category':
        articles = models.Article.objects.filter(category__id=value)
    elif field == 'tags':
        articles = models.Article.objects.filter(tags__id=value)
    else:
        return Http404()
    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    popular_articles = models.Article.objects.order_by('-views')[:3]
    context = {
        'articles': articles_page,
        'categories': categories,
        'tags': tags,
        'popular_articles': popular_articles,
    }
    return render(request, 'user/index.html', context)


def search(request):
    title = request.GET.get('title')
    q1 = Q(title__contains=title)
    q2 = Q(text__contains=title)
    articles = models.Article.objects.filter(q1 | q2)
    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    popular_articles = models.Article.objects.order_by('-views')[:3]
    context = {
        'articles': articles_page,
        'categories': categories,
        'tags': tags,
        'popular_articles': popular_articles,
    }
    return render(request, 'user/index.html', context)


def contact(request):
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()

    if request.method == 'GET':
        form = forms.ContactForm()
    elif request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            models.Contact.objects.create(name=form.cleaned_data['name'],
                                          title=form.cleaned_data['title'],
                                          email=form.cleaned_data['email'],
                                          text=form.cleaned_data['text']
                                          )
            return HttpResponseRedirect(reverse('index'))

    context = {'form': form,
               'categories': categories,
               'tags': tags,
               }
    return render(request, 'user/contact.html', context)


def notify(request):
    form = forms.NotifyForm(request.POST)
    if form.is_valid():
        models.Notify.objects.create(email=form.cleaned_data['email'])
    return JsonResponse({'hi': 'hi'})
