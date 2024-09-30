
# CRM Projekt

## Opis projektu

CRM Projekt to prosty system zarządzania relacjami z klientami stworzony w Django. Aplikacja umożliwia zarządzanie klientami, zamówieniami oraz generowanie raportów sprzedaży. Posiada system uwierzytelniania użytkowników z rolami i uprawnieniami.

## Funkcjonalności

- **Zarządzanie klientami**: dodawanie, edytowanie klientów.
- **Zarządzanie zamówieniami**: dodawanie, edytowanie zamówień.
- **Raport sprzedaży**: generowanie raportu z łączną kwotą sprzedaży.
- **System uwierzytelniania**: rejestracja, logowanie, wylogowanie użytkowników.
- **Role i uprawnienia**: różne poziomy dostępu dla administratorów, menedżerów i pracowników.
- **Interfejs użytkownika**: responsywny interfejs z wykorzystaniem Bootstrap.
- **Kolorowanie statusów zamówień**: zamówienia w realizacji (pomarańczowy), anulowane (czerwony), zrealizowane (zielony).

## Instalacja

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/TwojeRepozytorium/CRM-Projekt.git
   cd CRM-Projekt
   ```

2. **Utwórz i aktywuj wirtualne środowisko:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Na Windows: venv\Scripts\activate
   ```

3. **Zainstaluj wymagane pakiety:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Wykonaj migracje bazy danych:**

   ```bash
   python manage.py migrate
   ```

5. **Utwórz superużytkownika:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Uruchom serwer deweloperski:**

   ```bash
   python manage.py runserver
   ```

7. **Otwórz aplikację w przeglądarce:**

   ```
   http://127.0.0.1:8000/
   ```

## Użytkowanie

- **Rejestracja użytkownika:**
  - Przejdź do `/rejestracja/` lub kliknij "Zarejestruj się" na stronie głównej.
  - Wypełnij formularz rejestracji.
  - Po rejestracji użytkownik zostanie przypisany do grupy "Pracownicy".

- **Logowanie i wylogowanie:**
  - Logowanie dostępne pod `/login/` lub przez link "Zaloguj się".
  - Wylogowanie poprzez przycisk "Wyloguj się" w nawigacji (wymaga potwierdzenia przez formularz POST).

- **Zarządzanie klientami i zamówieniami:**
  - Dostępne dla użytkowników z odpowiednimi uprawnieniami.
  - Dodawanie i edycja poprzez formularze w interfejsie aplikacji.

- **Raport sprzedaży:**
  - Dostępny pod `/raport-sprzedazy/` lub przez link w nawigacji.
  - Wyświetla listę zamówień oraz łączną kwotę sprzedaży.

## Role i uprawnienia

- **Administratorzy:**
  - Pełne uprawnienia do zarządzania aplikacją.
  - Dostęp do panelu administracyjnego Django.

- **Menedżerowie:**
  - Mogą dodawać, edytować klientów i zamówienia.
  - Mają dostęp do raportów sprzedaży.

- **Pracownicy:**
  - Ograniczony dostęp.
  - Mogą przeglądać listę klientów i zamówień.

## Struktura projektu

- **crm_project/** - główny katalog projektu Django.
  - **settings.py** - ustawienia projektu.
  - **urls.py** - główne ścieżki URL projektu.

- **crm_app/** - aplikacja CRM.
  - **models.py** - definicje modeli danych.
  - **views.py** - logika widoków aplikacji.
  - **forms.py** - definicje formularzy.
  - **urls.py** - ścieżki URL aplikacji.
  - **templates/crm_app/** - szablony HTML aplikacji.
  - **static/crm_app/** - pliki statyczne (CSS, JS, obrazy).

- **templates/registration/** - szablony związane z uwierzytelnianiem (logowanie, wylogowanie).

## Technologie

- **Python 3.12.1**
- **Django 5.0.1**
- **Bootstrap 4.5.2**

## Dalszy rozwój

- **Testy jednostkowe**: Implementacja testów dla modeli, widoków i formularzy.
- **Integracje z API**: Dodanie integracji z zewnętrznymi usługami, np. API płatności, powiadomienia e-mail/SMS.
- **Optymalizacja**: Refaktoryzacja kodu, poprawa wydajności.
- **Wdrożenie**: Przygotowanie aplikacji do wdrożenia na serwer produkcyjny.
- **Międzynarodowość**: Dodanie wsparcia dla wielu języków (i18n).


