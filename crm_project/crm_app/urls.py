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
    path('raport-sprzedazy/', views.raport_sprzedazy, name='raport-sprzedazy'),
]
