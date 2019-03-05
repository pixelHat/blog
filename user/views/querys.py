from user import models


def get_latest_articles():
    return models.Article.objects.order_by('-published')


def get_popular_articles():
    return models.Article.objects.order_by('-views')[:3]


def get_related_articles(article):
    return models.Article.objects.filter(category__exact=article.category)\
                 .exclude(id__exact=article.id)
