from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Klient, Zamowienie, Produkt, Powiadomienie, ZamowienieProdukt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget

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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProduktForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ZamowienieProduktForm(forms.ModelForm):
    ilosc = forms.IntegerField(min_value=1, label='Ilość')

    class Meta:
        model = ZamowienieProdukt
        fields = ['produkt', 'ilosc']
        widgets = {
            'produkt': Select2Widget(attrs={'class': 'form-control'}),
        }

class ZamowienieForm(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = ['klient', 'status']
        widgets = {
            'klient': Select2Widget(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ZamowienieForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class RejestracjaForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RejestracjaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PowiadomienieForm(forms.ModelForm):
    class Meta:
        model = Powiadomienie
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PowiadomienieForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Inline formset for Zamowienie and ZamowienieProdukt
ZamowienieProduktFormSet = inlineformset_factory(
    Zamowienie, ZamowienieProdukt, form=ZamowienieProduktForm, extra=1, can_delete=True
)
