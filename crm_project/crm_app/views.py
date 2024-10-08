from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Klient, Zamowienie, Produkt, Powiadomienie, ZamowienieProdukt
from .forms import KlientForm, ZamowienieForm, RejestracjaForm, ProduktForm, PowiadomienieForm, ZamowienieProduktForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.utils.timezone import now
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.forms import inlineformset_factory
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@login_required
def dashboard(request):
    klienci = Klient.objects.all()
    zamowienia = Zamowienie.objects.all()

    # Filtracja zamówień według statusów
    zamowienia_zrealizowane = zamowienia.filter(status='zrealizowane')
    zamowienia_w_realizacji = zamowienia.filter(status='w_realizacji')
    zamowienia_anulowane = zamowienia.filter(status='anulowane')

    nowe_zamowienia_ilosc = zamowienia.filter(data_zamowienia__month=now().month).count()
    kwota_zrealizowanych = zamowienia_zrealizowane.aggregate(Sum('kwota'))['kwota__sum'] or 0
    nowi_klienci = klienci.filter(data_dodania__gte=now() - timedelta(days=30)).count()

    # Dodatkowe statystyki
    zamowienia_w_realizacji_ilosc = zamowienia_w_realizacji.count()
    anulowane_w_miesiacu = zamowienia_anulowane.filter(data_zamowienia__month=now().month).count()

    top_klient = zamowienia_zrealizowane.values('klient__imie', 'klient__nazwisko').annotate(total_kwota=Sum('kwota')).order_by('-total_kwota').first()

    # Pobieranie danych dla wykresów
    six_months_ago = now().replace(day=1) - timedelta(days=180)

    # Zamówienia w ostatnich 6 miesiącach
    last_six_months = zamowienia.filter(data_zamowienia__gte=six_months_ago) \
        .annotate(month=TruncMonth('data_zamowienia')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    last_six_months_kwota = zamowienia.filter(data_zamowienia__gte=six_months_ago) \
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
        'zamowienia_zrealizowane': zamowienia_zrealizowane,
        'zamowienia_w_realizacji': zamowienia_w_realizacji,
        'zamowienia_anulowane': zamowienia_anulowane,
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
    ZamowienieProduktFormSet = inlineformset_factory(
        Zamowienie, ZamowienieProdukt, form=ZamowienieProduktForm, extra=1
    )
    form = ZamowienieForm(request.POST or None)
    formset = ZamowienieProduktFormSet(request.POST or None)

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            zamowienie = form.save(commit=False)

            # Ustawienie tymczasowej kwoty 0 przed dodaniem produktów
            zamowienie.kwota = 0
            zamowienie.save()

            total_kwota = 0  # Inicjalizacja kwoty całkowitej zamówienia
            zamowienie_produkty = formset.save(commit=False)
            for zp in zamowienie_produkty:
                zp.zamowienie = zamowienie
                zp.save()
                total_kwota += zp.produkt.cena * zp.ilosc  # Obliczanie kwoty zamówienia na podstawie ceny i ilości

            zamowienie.kwota = total_kwota  # Ustawienie kwoty w zamówieniu
            zamowienie.save()

            return redirect('dashboard')

    context = {'form': form, 'formset': formset, 'title': 'Dodaj Zamówienie'}
    return render(request, 'crm_app/dodaj_zamowienie.html', context)


@login_required
@permission_required('crm_app.change_zamowienie', raise_exception=True)
def edytuj_zamowienie(request, pk):
    zamowienie = get_object_or_404(Zamowienie, id=pk)
    ZamowienieProduktFormSet = inlineformset_factory(
        Zamowienie, ZamowienieProdukt, form=ZamowienieProduktForm, extra=1
    )
    form = ZamowienieForm(instance=zamowienie)
    formset = ZamowienieProduktFormSet(instance=zamowienie)

    if request.method == 'POST':
        form = ZamowienieForm(request.POST, instance=zamowienie)
        formset = ZamowienieProduktFormSet(request.POST, instance=zamowienie)
        if form.is_valid() and formset.is_valid():
            zamowienie = form.save()
            formset.save()
            return redirect('dashboard')

    context = {'form': form, 'formset': formset, 'title': 'Edytuj Zamówienie'}
    return render(request, 'crm_app/dodaj_zamowienie.html', context)

def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    zamowienia_zrealizowane = Zamowienie.objects.filter(status='zrealizowane')
    zamowienia_anulowane = Zamowienie.objects.filter(status='anulowane')
    zamowienia_w_realizacji = Zamowienie.objects.filter(status='w_realizacji')

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

@login_required
@permission_required('crm_app.add_powiadomienie', raise_exception=True)
def dodaj_powiadomienie(request):
    form = PowiadomienieForm()
    if request.method == 'POST':
        form = PowiadomienieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form, 'title': 'Dodaj Powiadomienie'}
    return render(request, 'crm_app/form.html', context)

@login_required
def generuj_fakture(request, pk):
    zamowienie = get_object_or_404(Zamowienie, pk=pk)
    produkty = ZamowienieProdukt.objects.filter(zamowienie=zamowienie)

    # Ustawienia odpowiedzi dla pliku PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="faktura_{zamowienie.id}.pdf"'

    # Tworzenie obiektu PDF
    pdf = canvas.Canvas(response, pagesize=letter)

    # Ustawienia strony
    pdf.setTitle(f'Faktura {zamowienie.id}')
    pdf.drawString(100, 750, f"Faktura dla zamówienia: {zamowienie.id}")
    pdf.drawString(100, 735, f"Klient: {zamowienie.klient.imie} {zamowienie.klient.nazwisko}")
    pdf.drawString(100, 720, f"Data zamówienia: {zamowienie.data_zamowienia.strftime('%Y-%m-%d')}")

    # Tabela z produktami
    y_position = 690
    pdf.drawString(100, y_position, "Produkty:")
    y_position -= 20
    pdf.drawString(100, y_position, "Nazwa")
    pdf.drawString(300, y_position, "Ilość")
    pdf.drawString(400, y_position, "Cena za sztukę")
    pdf.drawString(500, y_position, "Kwota")

    # Lista produktów
    y_position -= 20
    total_kwota = 0
    for produkt in produkty:
        pdf.drawString(100, y_position, produkt.produkt.nazwa)
        pdf.drawString(300, y_position, str(produkt.ilosc))
        pdf.drawString(400, y_position, f"{produkt.produkt.cena} zł")
        kwota_produktu = produkt.cena_calkowita()
        pdf.drawString(500, y_position, f"{kwota_produktu} zł")
        y_position -= 20
        total_kwota += kwota_produktu

    # Kwota całkowita
    pdf.drawString(100, y_position - 20, f"Łączna kwota: {total_kwota} zł")

    # Zakończenie tworzenia pliku PDF
    pdf.save()

    return response