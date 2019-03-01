from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from user import models


def showComments(request):
    was_read_by_manager = Q(was_read_by_manager=False)
    is_on_the_waiting_list = Q(is_on_the_waiting_list=False)
    comments = models.Comment.objects.filter(was_read_by_manager & is_on_the_waiting_list)
    return render(request, 'manager/comments.html', {'comments': comments})


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
