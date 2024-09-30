from django.contrib import admin
from .models import Klient, Zamowienie, HistoriaKontaktu

admin.site.register(Klient)
admin.site.register(Zamowienie)
admin.site.register(HistoriaKontaktu)
