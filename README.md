# Aplikacja do zgłoszeń niezgodności / reklamacji

## Cel
Prosta aplikacja do rejestrowania i obsługi zgłoszeń niezgodności na produkcji.

## Model danych (v1)
Tabela `reklamacje` zawiera m.in.:
- data_zgloszenia
- tytul_zgloszenia
- opis
- ilosc
- status
- zglaszajacy
- kod_wyrobu
- nazwa_wyrobu
- kkw
- claim_number

Statusy:
- NOWE
- W_TRAKCIE
- ZAMKNIETE
- ODRZUCONE
