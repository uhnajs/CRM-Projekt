# crm_app/forms.py

from django.forms import ModelForm
from .models import Klient, Zamowienie

class KlientForm(ModelForm):
    class Meta:
        model = Klient
        fields = '__all__'

class ZamowienieForm(ModelForm):
    class Meta:
        model = Zamowienie
        fields = '__all__'
