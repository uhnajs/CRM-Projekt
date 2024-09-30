# crm_app/forms.py

from django import forms
from django.forms import ModelForm
from .models import Klient, Zamowienie
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class KlientForm(ModelForm):
    class Meta:
        model = Klient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(KlientForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ZamowienieForm(ModelForm):
    class Meta:
        model = Zamowienie
        fields = '__all__'

class RejestracjaForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
