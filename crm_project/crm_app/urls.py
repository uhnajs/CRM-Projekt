# crm_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dodaj-klienta/', views.dodaj_klienta, name='dodaj-klienta'),
    path('edytuj-klienta/<str:pk>/', views.edytuj_klienta, name='edytuj-klienta'),
    path('dodaj-zamowienie/', views.dodaj_zamowienie, name='dodaj-zamowienie'),
    path('edytuj-zamowienie/<str:pk>/', views.edytuj_zamowienie, name='edytuj-zamowienie'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('logout/', views.custom_logout, name='logout'),
    path('raport-sprzedazy/', views.raport_sprzedazy, name='raport-sprzedazy'),
    path('dodaj-produkt/', views.dodaj_produkt, name='dodaj-produkt'),
    path('dodaj-powiadomienie/', views.dodaj_powiadomienie, name='dodaj-powiadomienie'),
    path('generuj-fakture/<int:pk>/', views.generuj_fakture, name='generuj-fakture'),

]
