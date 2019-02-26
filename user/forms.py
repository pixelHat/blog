from django import forms


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
