# Šī rinda importē Blueprint maršrutu grupēšanai.
from flask import Blueprint

# Šī rinda importē render_template HTML lapu atgriešanai.
from flask import render_template

# Šī rinda importē current_user aktīvā lietotāja datiem.
from flask_login import current_user

# Šī rinda importē login_required piekļuves aizsardzībai.
from flask_login import login_required

# Šī rinda importē datubāzes iegūšanas funkciju.
from .db import iegut_db

# Šī rinda izveido blueprint lietotāja plāna skatiem.
bp = Blueprint("plans", __name__)

# Šī rinda definē maršrutu lietotāja plāna skatam.
@bp.route("/mans-plans")
# Šī rinda nodrošina, ka šo skatu redz tikai pieslēdzies lietotājs.
@login_required
# Šī funkcija atgriež konkrētā lietotāja treniņu plānu.
def mans_plans():
    # Šī rinda iegūst DB savienojumu.
    db = iegut_db()

    # Šī rinda atlasa lietotāja plāna ierakstus ar vingrinājumu nosaukumiem.
    rindas = db.execute(
        """
        SELECT
            treninu_plani.id,
            treninu_plani.nedelas_diena,
            treninu_plani.komplekti,
            treninu_plani.atkartojumi,
            treninu_plani.seciba,
            vingrinajumi.nosaukums
        FROM treninu_plani
        JOIN vingrinajumi ON treninu_plani.vingrinajums_id = vingrinajumi.id
        WHERE treninu_plani.lietotajs_id = ?
        ORDER BY treninu_plani.nedelas_diena, treninu_plani.seciba
        """,
        (current_user.id,)
    ).fetchall()

    # Šī rinda izveido vārdnīcu, kas grupē vingrinājumus pa nedēļas dienām.
    plani_pa_dienam = {
        "Pirmdiena": [],
        "Otrdiena": [],
        "Trešdiena": [],
        "Ceturtdiena": [],
        "Piektdiena": [],
        "Sestdiena": [],
        "Svētdiena": []
    }

    # Šī rinda izveido datu struktūru koda iekšējai dienu pārvēršanai.
    dienu_karti = {
        "MON": "Pirmdiena",
        "TUE": "Otrdiena",
        "WED": "Trešdiena",
        "THU": "Ceturtdiena",
        "FRI": "Piektdiena",
        "SAT": "Sestdiena",
        "SUN": "Svētdiena"
    }

    # Šī rinda iziet cauri katram planā atrastajam ierakstam.
    for rinda in rindas:
        # Šī rinda nosaka latvisko dienas nosaukumu.
        diena = dienu_karti.get(rinda["nedelas_diena"], rinda["nedelas_diena"])

        # Šī rinda pievieno konkrēto vingrinājuma ierakstu attiecīgajai dienai.
        plani_pa_dienam[diena].append(rinda)

    # Šī rinda atgriež lietotāja plāna HTML veidni.
    return render_template("mans_plans.html", plani_pa_dienam=plani_pa_dienam)
