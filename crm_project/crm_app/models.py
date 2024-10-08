from django.db import models

class Klient(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    adres = models.CharField(max_length=255)
    numer_telefonu = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    kategoria = models.CharField(max_length=10, choices=[
        ('nowy', 'Nowy'),
        ('staly', 'Stały'),
        ('VIP', 'VIP'),
    ])
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Produkt(models.Model):
    nazwa = models.CharField(max_length=255)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    opis = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nazwa


class Zamowienie(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    data_zamowienia = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=[
        ('w_realizacji', 'W realizacji'),
        ('zrealizowane', 'Zrealizowane'),
        ('anulowane', 'Anulowane'),
    ])
    kwota = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Zamówienie {self.id} - {self.klient}"


class ZamowienieProdukt(models.Model):
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.CASCADE, related_name='zamowienie_produkty')
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    ilosc = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produkt.nazwa} x {self.ilosc}"

    def cena_calkowita(self):
        return self.produkt.cena * self.ilosc


class HistoriaKontaktu(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    data_kontaktu = models.DateTimeField(auto_now_add=True)
    typ_kontaktu = models.CharField(max_length=15, choices=[
        ('telefon', 'Telefon'),
        ('email', 'E-mail'),
        ('spotkanie', 'Spotkanie'),
    ])
    notatka = models.TextField()

    def __str__(self):
        return f"Kontakt z {self.klient} dnia {self.data_kontaktu.strftime('%Y-%m-%d')}"


class Powiadomienie(models.Model):
    TYPY_POWIADOMIEN = [
        ('zadanie', 'Zadanie'),
        ('przypomnienie', 'Przypomnienie'),
        ('spotkanie', 'Spotkanie'),
    ]

    tytul = models.CharField(max_length=255)
    data = models.DateTimeField()
    opis = models.TextField(blank=True, null=True)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, blank=True, null=True)
    typ = models.CharField(max_length=20, choices=TYPY_POWIADOMIEN)

    def __str__(self):
        return f"{self.tytul} - {self.data.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-data']
