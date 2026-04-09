# Šī rinda importē Blueprint funkciju moduļa maršrutu grupēšanai.
from flask import Blueprint

# Šī rinda importē flash īslaicīgu ziņu parādīšanai.
from flask import flash

# Šī rinda importē redirect pāradresācijām.
from flask import redirect

# Šī rinda importē render_template HTML veidņu atgriešanai.
from flask import render_template

# Šī rinda importē request formas datu nolasīšanai.
from flask import request

# Šī rinda importē url_for maršrutu nosaukumu pārvēršanai adresēs.
from flask import url_for

# Šī rinda importē login_required aizsardzībai.
from flask_login import login_required

# Šī rinda importē login_user lietotāja pieslēgšanai.
from flask_login import login_user

# Šī rinda importē logout_user lietotāja izrakstīšanai.
from flask_login import logout_user

# Šī rinda importē check_password_hash paroles pārbaudei.
from werkzeug.security import check_password_hash

# Šī rinda importē generate_password_hash paroles drošai saglabāšanai.
from werkzeug.security import generate_password_hash

# Šī rinda importē DB iegūšanas funkciju.
from .db import iegut_db

# Šī rinda importē Lietotajs klasi.
from .models import Lietotajs

# Šī rinda izveido blueprint autentifikācijas maršrutiem.
bp = Blueprint("auth", __name__)

# Šī rinda definē reģistrācijas maršrutu.
@bp.route("/registreties", methods=["GET", "POST"])
# Šī funkcija apstrādā jauna lietotāja reģistrāciju.
def registreties():
    # Šī rinda pārbauda, vai forma nosūtīta ar POST metodi.
    if request.method == "POST":
        # Šī rinda nolasa lietotājvārdu no formas un noņem liekās atstarpes.
        lietotajvards = request.form.get("lietotajvards", "").strip()

        # Šī rinda nolasa lietotāja parasto vārdu.
        vards = request.form.get("vards", "").strip()

        # Šī rinda nolasa paroli no formas.
        parole = request.form.get("parole", "")

        # Šī rinda pārbauda, vai visi lauki ir aizpildīti.
        if not lietotajvards or not vards or not parole:
            # Šī rinda parāda kļūdas ziņu.
            flash("Lūdzu, aizpildi visus laukus.", "error")

            # Šī rinda atgriež reģistrācijas lapu no jauna.
            return render_template("registreties.html")

        # Šī rinda izveido drošu paroles hash, neglabājot paroli parastā tekstā.
        parole_hash = generate_password_hash(parole)

        # Šī rinda iegūst savienojumu ar datubāzi.
        db = iegut_db()

        # Šī rinda mēģina saglabāt lietotāju datubāzē.
        try:
            # Šī rinda izpilda drošu parametrizētu INSERT vaicājumu.
            db.execute(
                "INSERT INTO lietotaji (lietotajvards, vards, parole_hash, loma, izveidots) VALUES (?, ?, ?, ?, datetime('now'))",
                (lietotajvards, vards, parole_hash, "lietotajs")
            )

            # Šī rinda apstiprina datubāzes izmaiņas.
            db.commit()

        # Šī rinda noķer kļūdas, piemēram, ja lietotājvārds jau eksistē.
        except Exception:
            # Šī rinda parāda lietotājam kļūdas ziņu.
            flash("Šāds lietotājvārds jau pastāv.", "error")

            # Šī rinda atgriež reģistrācijas veidni.
            return render_template("registreties.html")

        # Šī rinda parāda veiksmīgas reģistrācijas paziņojumu.
        flash("Konts veiksmīgi izveidots. Tagad pieslēdzies.", "success")

        # Šī rinda novirza lietotāju uz pieslēgšanās lapu.
        return redirect(url_for("auth.pieslegties"))

    # Šī rinda atgriež reģistrācijas lapu GET pieprasījumam.
    return render_template("registreties.html")

# Šī rinda definē pieslēgšanās maršrutu.
@bp.route("/pieslegties", methods=["GET", "POST"])
# Šī funkcija apstrādā lietotāja pieslēgšanos.
def pieslegties():
    # Šī rinda pārbauda, vai forma nosūtīta.
    if request.method == "POST":
        # Šī rinda nolasa lietotājvārdu no formas.
        lietotajvards = request.form.get("lietotajvards", "").strip()

        # Šī rinda nolasa paroli no formas.
        parole = request.form.get("parole", "")

        # Šī rinda iegūst DB savienojumu.
        db = iegut_db()

        # Šī rinda atrod lietotāju datubāzē pēc lietotājvārda.
        rinda = db.execute(
            "SELECT id, lietotajvards, vards, parole_hash, loma FROM lietotaji WHERE lietotajvards = ?",
            (lietotajvards,)
        ).fetchone()

        # Šī rinda pārbauda, vai lietotājs tika atrasts.
        if rinda is None:
            # Šī rinda parāda vispārīgu kļūdas ziņu drošības dēļ.
            flash("Nepareizi pieslēgšanās dati.", "error")

            # Šī rinda atgriež pieslēgšanās lapu no jauna.
            return render_template("pieslegties.html")

        # Šī rinda pārbauda, vai ievadītā parole sakrīt ar hash.
        if not check_password_hash(rinda["parole_hash"], parole):
            # Šī rinda parāda kļūdu, ja parole nesakrīt.
            flash("Nepareizi pieslēgšanās dati.", "error")

            # Šī rinda atgriež pieslēgšanās lapu vēlreiz.
            return render_template("pieslegties.html")

        # Šī rinda pārvērš datubāzes rindu par Lietotajs objektu.
        lietotajs = Lietotajs.no_db_rindas(rinda)

        # Šī rinda ielogina lietotāju sesijā.
        login_user(lietotajs)

        # Šī rinda parāda veiksmīgas pieslēgšanās ziņu.
        flash("Tu veiksmīgi pieslēdzies sistēmai.", "success")

        # Šī rinda novirza lietotāju uz viņa plāna skatu.
        return redirect(url_for("plans.mans_plans"))

    # Šī rinda atgriež pieslēgšanās lapu GET pieprasījumam.
    return render_template("pieslegties.html")

# Šī rinda definē izrakstīšanās maršrutu.
@bp.route("/iziet", methods=["GET", "POST"])
# Šī rinda nodrošina, ka iziet var tikai pieslēdzies lietotājs.
@login_required
# Šī funkcija izraksta lietotāju no sistēmas.
def iziet():
    # Šī rinda izdzēš lietotāja sesiju.
    logout_user()

    # Šī rinda parāda informācijas paziņojumu.
    flash("Tu veiksmīgi izgāji no sistēmas.", "info")

    # Šī rinda novirza lietotāju uz sākumlapu.
    return redirect(url_for("index"))
