# Treniņu plāna un rezultātu sistēma

Šis ir skolas noslēguma projekts kursam **Programmēšana II**. Projekts izveidots ar **Python**, **Flask**, **SQLite**, **Flask-Login** un **Chart.js**.

## Projekta mērķis
Izveidot tīmekļa sistēmu, kur:
- lietotājs var apskatīt savu treniņu plānu;
- lietotājs var pievienot savus treniņu rezultātus;
- admins var pievienot vingrinājumus un veidot plānus lietotājiem;
- sistēmā ir lietotāju lomas un datu aizsardzība.

## Izmantotās tehnoloģijas
- Python
- Flask
- Flask-Login
- SQLite
- HTML / CSS / JavaScript
- Chart.js

## Kā palaist projektu

### 1. Izveido virtuālo vidi
```bash
python -m venv .venv
```

### 2. Aktivizē virtuālo vidi
Windows:
```bash
.venv\Scripts\activate
```

Mac / Linux:
```bash
source .venv/bin/activate
```

### 3. Uzinstalē bibliotēkas
```bash
pip install -r requirements.txt
```

### 4. Izveido testa datus
```bash
python seed_data.py
```

### 5. Palaid projektu
```bash
flask --app run.py run
```

## Testa lietotāji
- admins: `admin` / `admin123`
- lietotājs: `pauls` / `parole123`

## GitHub iesniegšanai
GitHub repozitorijā jāieliek **visa šī mapes struktūra atarhivētā veidā**, nevis tikai ZIP fails.
