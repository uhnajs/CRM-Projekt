# crm_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Klient, Zamowienie
from .forms import KlientForm, ZamowienieForm, RejestracjaForm
from django.contrib.auth import login, logout
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
            print("Zamówienie zapisane:", zamowienie)
            return redirect('dashboard')
        else:
            print("Błędy formularza:", form.errors)
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
    # Poprawne filtrowanie zamówień według statusów
    zamowienia_zrealizowane = Zamowienie.objects.filter(status='zrealizowane')
    zamowienia_anulowane = Zamowienie.objects.filter(status='anulowane')
    zamowienia_w_realizacji = Zamowienie.objects.filter(status='w_realizacji')

    # Łączna kwota tylko dla "Zrealizowane"
    laczna_kwota = sum(z.kwota for z in zamowienia_zrealizowane)

    context = {
        'zamowienia_zrealizowane': zamowienia_zrealizowane,
        'zamowienia_anulowane': zamowienia_anulowane,
        'zamowienia_w_realizacji': zamowienia_w_realizacji,
        'laczna_kwota': laczna_kwota,
    }

    return render(request, 'crm_app/raport_sprzedazy.html', context)

def custom_logout(request):
    logout(request)
    return redirect('login')
