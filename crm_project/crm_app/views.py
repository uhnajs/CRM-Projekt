from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Klient, Zamowienie
from .forms import KlientForm, ZamowienieForm, RejestracjaForm , ProduktForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.utils.timezone import now
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

@login_required
def dashboard(request):
    # Pobierz listę klientów i zamówień z bazy danych
    klienci = Klient.objects.all()
    zamowienia = Zamowienie.objects.all()

    # Statystyki główne
    nowe_zamowienia_ilosc = zamowienia.filter(data_zamowienia__month=now().month).count()
    kwota_zrealizowanych = zamowienia.filter(status='zrealizowane').aggregate(Sum('kwota'))['kwota__sum'] or 0
    nowi_klienci = klienci.filter(data_dodania__gte=now() - timedelta(days=30)).count()

    # Dodatkowe statystyki
    zamowienia_w_realizacji_ilosc = zamowienia.filter(status='w_realizacji').count()
    anulowane_w_miesiacu = zamowienia.filter(status='anulowane', data_zamowienia__month=now().month).count()

    # Top klient z największą kwotą zamówień
    top_klient = zamowienia.values('klient__imie', 'klient__nazwisko').annotate(total_kwota=Sum('kwota')).order_by('-total_kwota').first()

    # Pobieranie danych dla wykresów
    six_months_ago = now().replace(day=1) - timedelta(days=180)

    # Zamówienia w ostatnich 6 miesiącach
    last_six_months = Zamowienie.objects.filter(data_zamowienia__gte=six_months_ago) \
        .annotate(month=TruncMonth('data_zamowienia')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    last_six_months_kwota = Zamowienie.objects.filter(data_zamowienia__gte=six_months_ago) \
        .annotate(month=TruncMonth('data_zamowienia')) \
        .values('month') \
        .annotate(total_kwota=Sum('kwota')) \
        .order_by('month')

    context = {
        'klienci': klienci,
        'zamowienia': zamowienia,
        'nowe_zamowienia_ilosc': nowe_zamowienia_ilosc,
        'kwota_zrealizowanych': kwota_zrealizowanych,
        'nowi_klienci': nowi_klienci,
        # Dodatkowe statystyki
        'zamowienia_w_realizacji_ilosc': zamowienia_w_realizacji_ilosc,
        'anulowane_w_miesiacu': anulowane_w_miesiacu,
        'top_klient': top_klient,
        'last_six_months': last_six_months,
        'last_six_months_kwota': last_six_months_kwota,
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
            zamowienie = form.save(commit=False)
            zamowienie.save()
            form.save_m2m()  # Zapisz relacje wiele do wielu (produkty)
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

# crm_app/views.py

@login_required
@permission_required('crm_app.add_produkt', raise_exception=True)
def dodaj_produkt(request):
    form = ProduktForm()
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form, 'title': 'Dodaj Produkt'}
    return render(request, 'crm_app/form.html', context)
