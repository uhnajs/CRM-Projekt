# crm_app/forms.py

from django import forms
from django.forms import ModelForm
from .models import Klient, Zamowienie, Produkt
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

class ProduktForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = ['nazwa', 'cena', 'opis']

class ZamowienieForm(forms.ModelForm):
    produkty = forms.ModelMultipleChoiceField(queryset=Produkt.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Zamowienie
        fields = ['klient', 'produkty', 'status', 'kwota']

class RejestracjaForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
