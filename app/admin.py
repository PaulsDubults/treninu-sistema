# Šī rinda importē Blueprint maršrutu grupēšanai.
from flask import Blueprint

# Šī rinda importē flash paziņojumiem.
from flask import flash

# Šī rinda importē redirect pāradresācijām.
from flask import redirect

# Šī rinda importē render_template HTML veidņu atgriešanai.
from flask import render_template

# Šī rinda importē request formas datu nolasīšanai.
from flask import request

# Šī rinda importē url_for maršrutu adresēm.
from flask import url_for

# Šī rinda importē mūsu dekoratoru lomas pārbaudei.
from .decorators import loma_prasita

# Šī rinda importē DB iegūšanas funkciju.
from .db import iegut_db

# Šī rinda izveido blueprint admin sadaļai.
bp = Blueprint("admin", __name__)

# Šī rinda definē admin sākumlapas maršrutu.
@bp.route("/admin")
# Šī rinda atļauj pieeju tikai administratoram.
@loma_prasita("admins")
# Šī funkcija parāda admin paneli.
def admin_sakums():
    # Šī rinda atgriež admin sākuma HTML veidni.
    return render_template("admin.html")

# Šī rinda definē maršrutu vingrinājumu pārvaldībai.
@bp.route("/admin/vingrinajumi", methods=["GET", "POST"])
# Šī rinda aizsargā maršrutu ar administratora lomu.
@loma_prasita("admins")
# Šī funkcija ļauj adminam pievienot vingrinājumus.
def admin_vingrinajumi():
    # Šī rinda iegūst DB savienojumu.
    db = iegut_db()

    # Šī rinda pārbauda, vai pievienošanas forma tika nosūtīta.
    if request.method == "POST":
        # Šī rinda nolasa vingrinājuma nosaukumu.
        nosaukums = request.form.get("nosaukums", "").strip()

        # Šī rinda nolasa muskuļu grupu.
        muskulu_grupa = request.form.get("muskulu_grupa", "").strip()

        # Šī rinda nolasa aprakstu.
        apraksts = request.form.get("apraksts", "").strip()

        # Šī rinda pārbauda, vai nosaukums ir ievadīts.
        if not nosaukums:
            # Šī rinda parāda kļūdas paziņojumu.
            flash("Vingrinājuma nosaukums ir obligāts.", "error")

            # Šī rinda novirza atpakaļ uz to pašu lapu.
            return redirect(url_for("admin.admin_vingrinajumi"))

        # Šī rinda mēģina saglabāt jauno vingrinājumu datubāzē.
        try:
            # Šī rinda izpilda drošu INSERT vaicājumu.
            db.execute(
                "INSERT INTO vingrinajumi (nosaukums, muskulu_grupa, apraksts, aktivs) VALUES (?, ?, ?, 1)",
                (nosaukums, muskulu_grupa, apraksts)
            )

            # Šī rinda saglabā izmaiņas datubāzē.
            db.commit()

            # Šī rinda parāda veiksmīgu paziņojumu.
            flash("Vingrinājums veiksmīgi pievienots.", "success")

        # Šī rinda apstrādā kļūdu, ja šāds nosaukums jau eksistē.
        except Exception:
            # Šī rinda parāda kļūdas paziņojumu.
            flash("Šāds vingrinājums jau pastāv.", "error")

        # Šī rinda novirza atpakaļ uz vingrinājumu lapu.
        return redirect(url_for("admin.admin_vingrinajumi"))

    # Šī rinda atlasa visus vingrinājumus pārskatam.
    vingrinajumi = db.execute(
        "SELECT id, nosaukums, muskulu_grupa, apraksts, aktivs FROM vingrinajumi ORDER BY nosaukums"
    ).fetchall()

    # Šī rinda atgriež vingrinājumu pārvaldības lapu.
    return render_template("admin_vingrinajumi.html", vingrinajumi=vingrinajumi)

# Šī rinda definē maršrutu lietotāju sarakstam.
@bp.route("/admin/lietotaji")
# Šī rinda ļauj piekļuvi tikai administratoram.
@loma_prasita("admins")
# Šī funkcija parāda lietotāju sarakstu.
def admin_lietotaji():
    # Šī rinda iegūst DB savienojumu.
    db = iegut_db()

    # Šī rinda atlasa visus lietotājus no datubāzes.
    lietotaji = db.execute(
        "SELECT id, lietotajvards, vards, loma, izveidots FROM lietotaji ORDER BY id"
    ).fetchall()

    # Šī rinda atgriež lietotāju saraksta lapu.
    return render_template("admin_lietotaji.html", lietotaji=lietotaji)

# Šī rinda definē maršrutu plāna piešķiršanai.
@bp.route("/admin/plani", methods=["GET", "POST"])
# Šī rinda ļauj piekļuvi tikai administratoram.
@loma_prasita("admins")
# Šī funkcija ļauj administratoram pievienot plāna ierakstus.
def admin_plani():
    # Šī rinda iegūst DB savienojumu.
    db = iegut_db()

    # Šī rinda pārbauda, vai forma nosūtīta.
    if request.method == "POST":
        # Šī rinda nolasa lietotāja ID no formas.
        lietotajs_id = request.form.get("lietotajs_id", "").strip()

        # Šī rinda nolasa vingrinājuma ID.
        vingrinajums_id = request.form.get("vingrinajums_id", "").strip()

        # Šī rinda nolasa nedēļas dienu.
        nedelas_diena = request.form.get("nedelas_diena", "").strip()

        # Šī rinda nolasa komplektu skaitu.
        komplekti = request.form.get("komplekti", "").strip()

        # Šī rinda nolasa atkārtojumu skaitu.
        atkartojumi = request.form.get("atkartojumi", "").strip()

        # Šī rinda nolasa secības numuru.
        seciba = request.form.get("seciba", "1").strip()

        # Šī rinda pārbauda obligāto lauku aizpildi.
        if not lietotajs_id or not vingrinajums_id or not nedelas_diena or not komplekti or not atkartojumi:
            # Šī rinda parāda kļūdas paziņojumu.
            flash("Aizpildi visus plāna laukus.", "error")

            # Šī rinda novirza atpakaļ uz plānu lapu.
            return redirect(url_for("admin.admin_plani"))

        # Šī rinda izpilda INSERT vaicājumu plāna ierakstam.
        db.execute(
            """
            INSERT INTO treninu_plani
            (lietotajs_id, vingrinajums_id, nedelas_diena, komplekti, atkartojumi, seciba)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (int(lietotajs_id), int(vingrinajums_id), nedelas_diena, int(komplekti), int(atkartojumi), int(seciba))
        )

        # Šī rinda saglabā plāna ierakstu datubāzē.
        db.commit()

        # Šī rinda parāda veiksmīgu paziņojumu.
        flash("Plāna ieraksts veiksmīgi pievienots.", "success")

        # Šī rinda novirza atpakaļ uz plānu sadaļu.
        return redirect(url_for("admin.admin_plani"))

    # Šī rinda atlasa visus lietotājus, kuriem var piešķirt plānus.
    lietotaji = db.execute(
        "SELECT id, vards, lietotajvards FROM lietotaji WHERE loma = 'lietotajs' ORDER BY vards"
    ).fetchall()

    # Šī rinda atlasa visus vingrinājumus nolaižamajam sarakstam.
    vingrinajumi = db.execute(
        "SELECT id, nosaukums FROM vingrinajumi WHERE aktivs = 1 ORDER BY nosaukums"
    ).fetchall()

    # Šī rinda atlasa visus jau esošos plāna ierakstus tabulas pārskatam.
    plani = db.execute(
        """
        SELECT
            treninu_plani.id,
            treninu_plani.nedelas_diena,
            treninu_plani.komplekti,
            treninu_plani.atkartojumi,
            treninu_plani.seciba,
            lietotaji.vards,
            lietotaji.lietotajvards,
            vingrinajumi.nosaukums
        FROM treninu_plani
        JOIN lietotaji ON treninu_plani.lietotajs_id = lietotaji.id
        JOIN vingrinajumi ON treninu_plani.vingrinajums_id = vingrinajumi.id
        ORDER BY lietotaji.vards, treninu_plani.nedelas_diena, treninu_plani.seciba
        """
    ).fetchall()

    # Šī rinda atgriež admin plāna pārvaldības veidni.
    return render_template("admin_plani.html", lietotaji=lietotaji, vingrinajumi=vingrinajumi, plani=plani)
