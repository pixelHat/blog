from django.db import IntegrityError
from django.http import JsonResponse
from user import models
from user import forms


def notify(request):
    wasRegistered = True
    form = forms.NotifyForm(request.POST)
    if form.is_valid():
        try:
            models.Notify.objects.create(email=form.cleaned_data['email'])
        except IntegrityError:
            wasRegistered = False
    return JsonResponse({'wasRegistered': wasRegistered})
