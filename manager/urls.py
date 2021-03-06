from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.showComments, name='showComments'),
    path('comments/read/', views.readComment, name='readComment'),
    path('comments/delete/', views.deleteComment, name='deleteComment'),
    path('comments/add/waitList/', views.addWaitListComment, name='addWaitListComment'),
    path('comments/reply/', views.replyComment, name='replyComment'),
    path('comments/read/contact/', views.readContact, name='readContact'),
]
