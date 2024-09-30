# crm_app/views.py
from django.shortcuts import render, redirect
from .forms import KlientForm , ZamowienieForm
from django.shortcuts import render
from .models import Klient, Zamowienie

def dashboard(request):
    klienci = Klient.objects.all()
    zamowienia = Zamowienie.objects.all()
    context = {
        'klienci': klienci,
        'zamowienia': zamowienia,
    }
    return render(request, 'crm_app/dashboard.html', context)

def dodaj_klienta(request):
    form = KlientForm()
    if request.method == 'POST':
        form = KlientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'crm_app/klient_form.html', context)

def edytuj_klienta(request, pk):
    klient = Klient.objects.get(id=pk)
    form = KlientForm(instance=klient)
    if request.method == 'POST':
        form = KlientForm(request.POST, instance=klient)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'crm_app/klient_form.html', context)

def dodaj_zamowienie(request):
    form = ZamowienieForm()
    if request.method == 'POST':
        form = ZamowienieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'crm_app/zamowienie_form.html', context)

def edytuj_zamowienie(request, pk):
    zamowienie = Zamowienie.objects.get(id=pk)
    form = ZamowienieForm(instance=zamowienie)
    if request.method == 'POST':
        form = ZamowienieForm(request.POST, instance=zamowienie)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'crm_app/zamowienie_form.html', context)
