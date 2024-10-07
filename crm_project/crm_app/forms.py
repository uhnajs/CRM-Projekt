from django import forms
from django.forms import ModelForm
from .models import Klient, Zamowienie, Produkt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget

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

class ZamowienieForm(forms.ModelForm):
    produkty = forms.ModelMultipleChoiceField(
        queryset=Produkt.objects.all().order_by('nazwa'),  # Sortowanie alfabetyczne
        widget=Select2MultipleWidget(attrs={'class': 'form-control'}),  # Widget z wyszukiwarką
        label="Produkty"
    )

    class Meta:
        model = Zamowienie
        fields = ['klient', 'produkty', 'status', 'kwota']

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
