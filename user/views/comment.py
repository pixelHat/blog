from django.http import JsonResponse
from user import models
from user import forms


def comment(request):
    json_response = {'ok': False}
    form = forms.CommentForm(request.POST)
    if form.is_valid():
        json_response = {'ok': True}
        reply = form.cleaned_data['reply']
        article = models.Article.objects.get(pk=form.cleaned_data['article'])
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        user = models.User.create_or_get(models.User, name=name, email=email)
        if not reply:
            models.Comment.objects.create(article=article, user=user,
                                          comment=message)
        else:
            models.Comment.objects.create(article=article,
                                          user=user,
                                          reply_id=reply,
                                          comment=message)
    return JsonResponse(json_response)
