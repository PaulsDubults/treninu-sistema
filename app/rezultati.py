# Šī rinda importē Blueprint maršrutu grupēšanai.
from flask import Blueprint

# Šī rinda importē flash paziņojumiem.
from flask import flash

# Šī rinda importē jsonify JSON atbilžu izveidei.
from flask import jsonify

# Šī rinda importē redirect pāradresācijām.
from flask import redirect

# Šī rinda importē render_template HTML lapu atgriešanai.
from flask import render_template

# Šī rinda importē request formas un URL parametru nolasīšanai.
from flask import request

# Šī rinda importē url_for maršrutu adresēm.
from flask import url_for

# Šī rinda importē current_user aktīvā lietotāja iegūšanai.
from flask_login import current_user

# Šī rinda importē login_required, lai aizsargātu skatus.
from flask_login import login_required

# Šī rinda importē DB iegūšanas funkciju.
from .db import iegut_db

# Šī rinda izveido rezultātu blueprint.
bp = Blueprint("rezultati", __name__)

# Šī rinda definē maršrutu rezultātu sarakstam.
@bp.route("/rezultati")
# Šī rinda nodrošina, ka skats pieejams tikai pieslēgtam lietotājam.
@login_required
# Šī funkcija parāda lietotāja rezultātus.
def skatit_rezultatus():
    # Šī rinda iegūst DB savienojumu.
    db = iegut_db()

    # Šī rinda atlasa visus konkrētā lietotāja rezultātus ar vingrinājuma nosaukumu.
    rezultati = db.execute(
        """
        SELECT
            rezultati.id,
            rezultati.datums,
            rezultati.svars_kg,
            rezultati.atkartojumi,
            rezultati.komplekti,
            rezultati.piezimes,
            vingrinajumi.id AS vingrinajums_id,
            vingrinajumi.nosaukums
        FROM rezultati
        JOIN vingrinajumi ON rezultati.vingrinajums_id = vingrinajumi.id
        WHERE rezultati.lietotajs_id = ?
        ORDER BY rezultati.datums DESC, rezultati.id DESC
        """,
        (current_user.id,)
    ).fetchall()

    # Šī rinda atlasa visus aktīvos vingrinājumus filtra sarakstam.
    vingrinajumi = db.execute(
        "SELECT id, nosaukums FROM vingrinajumi WHERE aktivs = 1 ORDER BY nosaukums"
    ).fetchall()

    # Šī rinda atgriež rezultātu HTML veidni.
    return render_template("rezultati.html", rezultati=rezultati, vingrinajumi=vingrinajumi)

# Šī rinda definē rezultāta pievienošanas maršrutu.
@bp.route("/rezultati/pievienot", methods=["GET", "POST"])
# Šī rinda aizsargā maršrutu ar autorizāciju.
@login_required
# Šī funkcija ļauj lietotājam pievienot jaunu rezultātu.
def pievienot_rezultatu():
    # Šī rinda iegūst DB savienojumu.
    db = iegut_db()

    # Šī rinda atlasa vingrinājumus nolaižamajam sarakstam.
    vingrinajumi = db.execute(
        "SELECT id, nosaukums FROM vingrinajumi WHERE aktivs = 1 ORDER BY nosaukums"
    ).fetchall()

    # Šī rinda pārbauda, vai forma ir nosūtīta.
    if request.method == "POST":
        # Šī rinda nolasa vingrinājuma ID no formas.
        vingrinajums_id = request.form.get("vingrinajums_id", "").strip()

        # Šī rinda nolasa datumu no formas.
        datums = request.form.get("datums", "").strip()

        # Šī rinda nolasa svaru kilogramos.
        svars_kg = request.form.get("svars_kg", "0").strip()

        # Šī rinda nolasa atkārtojumu skaitu.
        atkartojumi = request.form.get("atkartojumi", "").strip()

        # Šī rinda nolasa komplektu skaitu.
        komplekti = request.form.get("komplekti", "1").strip()

        # Šī rinda nolasa piezīmes no formas.
        piezimes = request.form.get("piezimes", "").strip()

        # Šī rinda pārbauda, vai obligātie lauki ir aizpildīti.
        if not vingrinajums_id or not datums or not atkartojumi:
            # Šī rinda parāda kļūdas ziņu.
            flash("Lūdzu, aizpildi obligātos laukus.", "error")

            # Šī rinda atgriež formu atkārtotai aizpildei.
            return render_template("pievienot_rezultatu.html", vingrinajumi=vingrinajumi)

        # Šī rinda mēģina pārveidot tekstu skaitliskās vērtībās.
        try:
            # Šī rinda pārvērš vingrinājuma ID par veselu skaitli.
            vingrinajums_id = int(vingrinajums_id)

            # Šī rinda pārvērš svaru par komatskaitli.
            svars_kg = float(svars_kg)

            # Šī rinda pārvērš atkārtojumus par veselu skaitli.
            atkartojumi = int(atkartojumi)

            # Šī rinda pārvērš komplektus par veselu skaitli.
            komplekti = int(komplekti)

        # Šī rinda apstrādā gadījumus, kad skaitļi ievadīti nepareizi.
        except ValueError:
            # Šī rinda parāda kļūdas paziņojumu.
            flash("Skaitliskajos laukos jāievada derīgas vērtības.", "error")

            # Šī rinda atgriež formu.
            return render_template("pievienot_rezultatu.html", vingrinajumi=vingrinajumi)

        # Šī rinda izpilda drošu INSERT vaicājumu datubāzē.
        db.execute(
            """
            INSERT INTO rezultati
            (lietotajs_id, vingrinajums_id, datums, svars_kg, atkartojumi, komplekti, piezimes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (current_user.id, vingrinajums_id, datums, svars_kg, atkartojumi, komplekti, piezimes)
        )

        # Šī rinda saglabā izmaiņas datubāzē.
        db.commit()

        # Šī rinda parāda veiksmīgas saglabāšanas paziņojumu.
        flash("Rezultāts veiksmīgi saglabāts.", "success")

        # Šī rinda novirza lietotāju uz rezultātu sarakstu.
        return redirect(url_for("rezultati.skatit_rezultatus"))

    # Šī rinda atgriež rezultāta pievienošanas lapu GET pieprasījumam.
    return render_template("pievienot_rezultatu.html", vingrinajumi=vingrinajumi)

# Šī rinda definē JSON API grafika datiem.
@bp.route("/api/rezultati/vingrinajums/<int:vingrinajums_id>")
# Šī rinda aizsargā API ar autorizāciju.
@login_required
# Šī funkcija atgriež konkrēta vingrinājuma progresu JSON formā.
def api_rezultati_vingrinajumam(vingrinajums_id):
    # Šī rinda iegūst DB savienojumu.
    db = iegut_db()

    # Šī rinda atlasa konkrētā lietotāja rezultātus izvēlētajam vingrinājumam.
    rindas = db.execute(
        """
        SELECT datums, svars_kg
        FROM rezultati
        WHERE lietotajs_id = ? AND vingrinajums_id = ?
        ORDER BY datums ASC, id ASC
        """,
        (current_user.id, vingrinajums_id)
    ).fetchall()

    # Šī rinda izveido sarakstu ar datumiem Chart.js X asij.
    labels = [rinda["datums"] for rinda in rindas]

    # Šī rinda izveido sarakstu ar svara datiem Chart.js Y asij.
    data = [rinda["svars_kg"] for rinda in rindas]

    # Šī rinda atgriež datus JSON formātā.
    return jsonify({"labels": labels, "data": data})
