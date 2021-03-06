from django.urls import path
import user.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:id>', views.article, name='article'),
    path('search/<str:field>&<str:value>', views.search_field, name='search_field'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('notify/', views.notify, name='notify'),
    path('comment/', views.comment, name='comment'),
]
