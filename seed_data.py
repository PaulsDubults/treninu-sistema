# Šī rinda importē sqlite3 moduli datubāzes darbībām.
import sqlite3

# Šī rinda importē os moduli failu ceļiem.
import os

# Šī rinda importē pathlib Path klasi mapju izveidei.
from pathlib import Path

# Šī rinda importē generate_password_hash drošai paroļu saglabāšanai.
from werkzeug.security import generate_password_hash

# Šī rinda nosaka projekta pamatmapi.
PAMATMAPE = Path(__file__).resolve().parent

# Šī rinda nosaka instance mapes ceļu.
INSTANCE_MAPE = PAMATMAPE / "instance"

# Šī rinda izveido instance mapi, ja tā neeksistē.
INSTANCE_MAPE.mkdir(parents=True, exist_ok=True)

# Šī rinda nosaka datubāzes faila ceļu.
DB_CELS = INSTANCE_MAPE / "treninu_sistema.db"

# Šī rinda nosaka shēmas faila ceļu.
SCHEMA_CELS = PAMATMAPE / "app" / "schema.sql"

# Šī funkcija inicializē datubāzi un pievieno testa datus.
def galvenais():
    # Šī rinda atver savienojumu ar SQLite datubāzi.
    db = sqlite3.connect(DB_CELS)

    # Šī rinda ieslēdz ārējo atslēgu pārbaudi.
    db.execute("PRAGMA foreign_keys = ON;")

    # Šī rinda atver schema.sql failu.
    with open(SCHEMA_CELS, "r", encoding="utf-8") as fails:
        # Šī rinda izpilda visus SQL vaicājumus no shēmas faila.
        db.executescript(fails.read())

    # Šī rinda sagatavo administratora paroles hash.
    admin_hash = generate_password_hash("admin123")

    # Šī rinda sagatavo parasta lietotāja paroles hash.
    pauls_hash = generate_password_hash("parole123")

    # Šī rinda ievieto administratoru datubāzē.
    db.execute(
        "INSERT INTO lietotaji (lietotajvards, vards, parole_hash, loma, izveidots) VALUES (?, ?, ?, ?, datetime('now'))",
        ("admin", "Administrators", admin_hash, "admins")
    )

    # Šī rinda ievieto parasto lietotāju datubāzē.
    db.execute(
        "INSERT INTO lietotaji (lietotajvards, vards, parole_hash, loma, izveidots) VALUES (?, ?, ?, ?, datetime('now'))",
        ("pauls", "Pauls Dubults", pauls_hash, "lietotajs")
    )

    # Šī rinda sagatavo vingrinājumu sarakstu pievienošanai.
    vingrinajumi = [
        ("Bench Press", "Krūtis", "Spiešana guļus ar stieni."),
        ("Squat", "Kājas", "Pietupiens ar stieni."),
        ("Barbell Row", "Mugura", "Vilce pie jostas ar stieni."),
        ("Shoulder Press", "Pleci", "Spiešana virs galvas."),
        ("Biceps Curl", "Rokas", "Bicepsa vingrinājums ar hantelēm.")
    ]

    # Šī rinda iziet cauri visiem vingrinājumiem sarakstā.
    for nosaukums, muskulu_grupa, apraksts in vingrinajumi:
        # Šī rinda ievieto vienu vingrinājumu datubāzē.
        db.execute(
            "INSERT INTO vingrinajumi (nosaukums, muskulu_grupa, apraksts, aktivs) VALUES (?, ?, ?, 1)",
            (nosaukums, muskulu_grupa, apraksts)
        )

    # Šī rinda pievieno plāna ierakstus lietotājam ar ID 2.
    db.execute("INSERT INTO treninu_plani (lietotajs_id, vingrinajums_id, nedelas_diena, komplekti, atkartojumi, seciba) VALUES (2, 1, 'MON', 4, 6, 1)")
    db.execute("INSERT INTO treninu_plani (lietotajs_id, vingrinajums_id, nedelas_diena, komplekti, atkartojumi, seciba) VALUES (2, 3, 'MON', 4, 8, 2)")
    db.execute("INSERT INTO treninu_plani (lietotajs_id, vingrinajums_id, nedelas_diena, komplekti, atkartojumi, seciba) VALUES (2, 2, 'WED', 4, 5, 1)")
    db.execute("INSERT INTO treninu_plani (lietotajs_id, vingrinajums_id, nedelas_diena, komplekti, atkartojumi, seciba) VALUES (2, 4, 'FRI', 3, 8, 1)")
    db.execute("INSERT INTO treninu_plani (lietotajs_id, vingrinajums_id, nedelas_diena, komplekti, atkartojumi, seciba) VALUES (2, 5, 'FRI', 3, 12, 2)")

    # Šī rinda pievieno dažus rezultātu ierakstus, lai grafikam būtu dati.
    db.execute("INSERT INTO rezultati (lietotajs_id, vingrinajums_id, datums, svars_kg, atkartojumi, komplekti, piezimes) VALUES (2, 1, '2026-03-20', 80, 6, 4, 'Labs treniņš')")
    db.execute("INSERT INTO rezultati (lietotajs_id, vingrinajums_id, datums, svars_kg, atkartojumi, komplekti, piezimes) VALUES (2, 1, '2026-03-27', 82.5, 6, 4, 'Neliels progress')")
    db.execute("INSERT INTO rezultati (lietotajs_id, vingrinajums_id, datums, svars_kg, atkartojumi, komplekti, piezimes) VALUES (2, 1, '2026-04-03', 85, 5, 4, 'Smagāks treniņš')")

    # Šī rinda saglabā visas izmaiņas datubāzē.
    db.commit()

    # Šī rinda aizver datubāzes savienojumu.
    db.close()

    # Šī rinda izvada veiksmīgu paziņojumu terminālī.
    print(f"Datubāze izveidota: {DB_CELS}")

# Šī rinda pārbauda, vai fails palaists tieši, nevis importēts.
if __name__ == "__main__":
    # Šī rinda izsauc galveno funkciju.
    galvenais()
