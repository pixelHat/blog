from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from user import models
from user import forms


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
