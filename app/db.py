# Šī rinda importē sqlite3 moduli darbam ar SQLite datubāzi.
import sqlite3

# Šī rinda importē click bibliotēku komandrindas komandai.
import click

# Šī rinda importē current_app un g no Flask.
from flask import current_app, g

# Šī funkcija atgriež aktīvo datubāzes savienojumu.
def iegut_db():
    # Šī rinda pārbauda, vai request kontekstā savienojums jau ir izveidots.
    if "db" not in g:
        # Šī rinda atver jaunu savienojumu ar SQLite failu.
        g.db = sqlite3.connect(
            # Šī rinda paņem datubāzes ceļu no konfigurācijas.
            current_app.config["DATABASE"],
            # Šī rinda ieslēdz deklarēto datu tipu atpazīšanu.
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # Šī rinda ļauj rezultātu rindas izmantot kā vārdnīcām līdzīgus objektus.
        g.db.row_factory = sqlite3.Row

        # Šī rinda ieslēdz ārējo atslēgu pārbaudi SQLite datubāzē.
        g.db.execute("PRAGMA foreign_keys = ON;")

    # Šī rinda atgriež jau izveidoto vai tikko atvērto savienojumu.
    return g.db

# Šī funkcija aizver datubāzes savienojumu request beigās.
def aizvert_db(e=None):
    # Šī rinda izņem savienojumu no Flask g objekta.
    db = g.pop("db", None)

    # Šī rinda pārbauda, vai savienojums eksistē.
    if db is not None:
        # Šī rinda aizver savienojumu.
        db.close()

# Šī funkcija inicializē datubāzi no schema.sql faila.
def init_db():
    # Šī rinda iegūst savienojumu ar datubāzi.
    db = iegut_db()

    # Šī rinda atver shēmas failu lasīšanas režīmā ar UTF-8 kodējumu.
    with current_app.open_resource("schema.sql", mode="r", encoding="utf-8") as f:
        # Šī rinda izpilda visus SQL vaicājumus no faila.
        db.executescript(f.read())

# Šī dekorētā funkcija izveido Flask komandu datubāzes inicializēšanai.
@click.command("init-db")
def init_db_command():
    # Šī rinda izsauc datubāzes inicializācijas funkciju.
    init_db()

    # Šī rinda izvada komandrindā paziņojumu par veiksmīgu darbību.
    click.echo("Datubāze ir inicializēta.")

# Šī funkcija reģistrē DB saistītās darbības Flask lietotnē.
def init_app(app):
    # Šī rinda pasaka Flask izsaukt savienojuma aizvēršanu katra request beigās.
    app.teardown_appcontext(aizvert_db)

    # Šī rinda pievieno komandrindas komandu init-db.
    app.cli.add_command(init_db_command)
