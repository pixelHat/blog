from django import forms
from django.core.exceptions import ObjectDoesNotExist


class ContactForm(forms.Form):
    attrs = {'class': 'input', 'placeholder': 'este campo é obrigatório.'}
    attrs_text = {'class': 'textarea',
                  'placeholder': 'este campo é obrigatório.',
                  }
    name = forms.CharField(max_length=100,
                           label='Nome',
                           widget=forms.TextInput(attrs=attrs))
    title = forms.CharField(max_length=100,
                            label='Título',
                            widget=forms.TextInput(attrs=attrs))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs=attrs))
    text = forms.CharField(label='Mensagem',
                           widget=forms.Textarea(attrs=attrs_text))


class NotifyForm(forms.Form):
    attrs = {'class': 'input', 'placeholder': 'email'}
    email = forms.EmailField(widget=forms.EmailInput(attrs=attrs))


class CommentForm(forms.Form):
    from .models import Article, Comment
    attrs = {'class': 'input'}
    name = forms.CharField(label='Nome',
                           max_length=70,
                           widget=forms.TextInput(attrs=attrs))
    email = forms.CharField(label='Email',
                            max_length=100,
                            widget=forms.EmailInput(attrs=attrs))
    message = forms.CharField(label='Mensagem',
                              widget=forms.Textarea(attrs={'class': 'textarea'}))
    article = forms.CharField(widget=forms.HiddenInput())
    reply = forms.CharField(widget=forms.HiddenInput())

    def clean_article(self):
        article = self.cleaned_data.get('article')
        try:
            self.Article.objects.get(pk=article)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Invalid article',
                                        code='invalid article')
        return article

    def clean_reply(self):
        reply = self.cleaned_data.get('reply')
        try:
            self.Comment.objects.get(pk=reply)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Invalid comment id',
                                        code='invalid comment id')
        return reply
