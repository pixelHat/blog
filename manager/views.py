from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from user import models


def showComments(request):
    was_read_by_manager = Q(was_read_by_manager=False)
    is_on_the_waiting_list = Q(is_on_the_waiting_list=False)
    new_comments = models.Comment.objects.filter(was_read_by_manager
                                                 & is_on_the_waiting_list)
    was_read_by_manager = Q(was_read_by_manager=False)
    is_on_the_waiting_list = Q(is_on_the_waiting_list=True)
    waiting_comments = models.Comment.objects\
                             .filter(was_read_by_manager
                                     & is_on_the_waiting_list)
    context = {
        'new_comments': new_comments,
        'waiting_comments': waiting_comments,
    }
    return render(request, 'manager/comments.html', context)


def readComment(request):
    try:
        id = request.GET.get('id')
        comment = models.Comment.objects.get(pk=id)
        comment.was_read_by_manager = True
        comment.save()
        context = {'ok': True}
    except (KeyError, ObjectDoesNotExist) as _:
        context = {'ok': False}
    return JsonResponse(context)


def deleteComment(request):
    try:
        id = request.GET.get('id')
        comment = models.Comment.objects.get(pk=id)
        comment.delete()
        context = {'ok': True}
    except (KeyError, ObjectDoesNotExist) as _:
        context = {'ok': False}
    return JsonResponse(context)


def addWaitListComment(request):
    try:
        id = request.GET.get('id')
        comment = models.Comment.objects.get(pk=id)
        comment.is_on_the_waiting_list = True
        comment.save()
        context = {'ok': True}
    except (KeyError, ObjectDoesNotExist) as _:
        context = {'ok': False}
    return JsonResponse(context)


def replyComment(request):
    try:
        user = models.User.objects.get(email='admin@admin.com')
        comment_id = request.GET.get('comment_id')
        text = request.GET.get('text')
        comment = models.Comment.objects.get(pk=comment_id)
        models.Reply.objects.create(user=user,
                                    comment_id=comment,
                                    comment=text,
                                    published=datetime.now())
        context = {'ok': True}
    except (KeyError, ObjectDoesNotExist) as _:
        context = {'ok': False}
    return JsonResponse(context)
