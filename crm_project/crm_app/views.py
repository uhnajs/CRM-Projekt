# crm_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Klient, Zamowienie
from .forms import KlientForm, ZamowienieForm, RejestracjaForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings

@login_required
def dashboard(request):
    klienci = Klient.objects.all()
    zamowienia = Zamowienie.objects.all()
    context = {
        'klienci': klienci,
        'zamowienia': zamowienia,
    }
    return render(request, 'crm_app/dashboard.html', context)

@login_required
@permission_required('crm_app.add_klient', raise_exception=True)
def dodaj_klienta(request):
    form = KlientForm()
    if request.method == 'POST':
        form = KlientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form, 'title': 'Dodaj Klienta'}
    return render(request, 'crm_app/form.html', context)

@login_required
@permission_required('crm_app.change_klient', raise_exception=True)
def edytuj_klienta(request, pk):
    klient = get_object_or_404(Klient, id=pk)
    form = KlientForm(instance=klient)
    if request.method == 'POST':
        form = KlientForm(request.POST, instance=klient)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form, 'title': 'Edytuj Klienta'}
    return render(request, 'crm_app/form.html', context)

@login_required
@permission_required('crm_app.add_zamowienie', raise_exception=True)
def dodaj_zamowienie(request):
    form = ZamowienieForm()
    if request.method == 'POST':
        form = ZamowienieForm(request.POST)
        if form.is_valid():
            zamowienie = form.save()
            # Opcjonalnie: Wysyłanie e-maila potwierdzającego
            # temat = 'Potwierdzenie zamówienia'
            # wiadomosc = f'Dziękujemy za zamówienie nr {zamowienie.id}.'
            # odbiorca = [zamowienie.klient.email]
            # send_mail(temat, wiadomosc, settings.DEFAULT_FROM_EMAIL, odbiorca)
            return redirect('dashboard')
    context = {'form': form, 'title': 'Dodaj Zamówienie'}
    return render(request, 'crm_app/form.html', context)

@login_required
@permission_required('crm_app.change_zamowienie', raise_exception=True)
def edytuj_zamowienie(request, pk):
    zamowienie = get_object_or_404(Zamowienie, id=pk)
    form = ZamowienieForm(instance=zamowienie)
    if request.method == 'POST':
        form = ZamowienieForm(request.POST, instance=zamowienie)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form, 'title': 'Edytuj Zamówienie'}
    return render(request, 'crm_app/form.html', context)

def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Przypisanie użytkownika do domyślnej grupy
            grupa = Group.objects.get(name='Pracownicy')
            user.groups.add(grupa)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RejestracjaForm()
    context = {'form': form}
    return render(request, 'crm_app/rejestracja.html', context)

@login_required
def raport_sprzedazy(request):
    zamowienia = Zamowienie.objects.all()
    total_kwota = sum(z.kwota for z in zamowienia)
    context = {
        'zamowienia': zamowienia,
        'total_kwota': total_kwota,
    }
    return render(request, 'crm_app/raport_sprzedazy.html', context)
