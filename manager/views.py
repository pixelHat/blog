from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from functools import reduce
import operator
from user import models


def showComments(request):
    query_new_comments_list = [Q(was_read_by_manager=False),
                               Q(is_on_the_waiting_list=False)]
    query_new_comments = reduce(operator.and_, query_new_comments_list)
    new_comments = models.Comment.objects.filter(query_new_comments)
    query_waiting_comments_list = [Q(was_read_by_manager=False),
                                   Q(is_on_the_waiting_list=True)]
    query_waiting_comments = reduce(operator.and_, query_waiting_comments_list)
    waiting_comments = models.Comment.objects.filter(query_waiting_comments)
    print(waiting_comments)
    json_response = {
        'new_comments': new_comments,
        'waiting_comments': waiting_comments,
        'contacts': models.Contact.objects.filter(was_read_by_manager=False)
    }
    return render(request, 'manager/comments.html', json_response)


def readComment(request):
    try:
        id = request.GET.get('id')
        comment = models.Comment.objects.get(pk=id)
        comment.was_read_by_manager = True
        comment.save()
        json_response = {'ok': True}
    except (KeyError, ObjectDoesNotExist):
        json_response = {'ok': False}
    return JsonResponse(json_response)


def deleteComment(request):
    try:
        id = request.GET.get('id')
        comment = models.Comment.objects.get(pk=id)
        comment.delete()
        json_response = {'ok': True}
    except (KeyError, ObjectDoesNotExist):
        json_response = {'ok': False}
    return JsonResponse(json_response)


def addWaitListComment(request):
    try:
        id = request.GET.get('id')
        comment = models.Comment.objects.get(pk=id)
        comment.is_on_the_waiting_list = True
        comment.save()
        json_response = {'ok': True}
    except (KeyError, ObjectDoesNotExist):
        json_response = {'ok': False}
    return JsonResponse(json_response)


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
        json_response = {'ok': True}
    except (KeyError, ObjectDoesNotExist):
        json_response = {'ok': False}
    return JsonResponse(json_response)


def readContact(request):
    try:
        id = request.GET.get('id')
        contact = models.Contact.objects.get(pk=id)
        contact.was_read_by_manager = True
        contact.save()
        json_response = {'ok': True}
    except (ObjectDoesNotExist, KeyError):
        json_response = {'ok': False}
    return JsonResponse(json_response)
