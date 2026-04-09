# Šī rinda importē UserMixin no Flask-Login, lai lietotāja klase atbilstu prasībām.
from flask_login import UserMixin

# Šī rinda importē DB iegūšanas funkciju.
from .db import iegut_db

# Šī klase apraksta sistēmas lietotāju.
class Lietotajs(UserMixin):
    # Šī metode inicializē jaunu Lietotajs objektu.
    def __init__(self, id, lietotajvards, vards, parole_hash, loma):
        # Šī rinda saglabā lietotāja ID objektā.
        self.id = id

        # Šī rinda saglabā lietotājvārdu objektā.
        self.lietotajvards = lietotajvards

        # Šī rinda saglabā lietotāja vārdu objektā.
        self.vards = vards

        # Šī rinda saglabā paroles hash objektā.
        self.parole_hash = parole_hash

        # Šī rinda saglabā lietotāja lomu objektā.
        self.loma = loma

    # Šī statiskā metode izveido Lietotajs objektu no DB rindas.
    @staticmethod
    def no_db_rindas(rinda):
        # Šī rinda pārbauda, vai DB rinda vispār eksistē.
        if rinda is None:
            # Šī rinda atgriež None, ja lietotājs nav atrasts.
            return None

        # Šī rinda izveido un atgriež jaunu Lietotajs objektu no rindas datiem.
        return Lietotajs(rinda["id"], rinda["lietotajvards"], rinda["vards"], rinda["parole_hash"], rinda["loma"])

    # Šī statiskā metode atrod lietotāju pēc ID.
    @staticmethod
    def atrast_pec_id(lietotaja_id):
        # Šī rinda iegūst DB savienojumu.
        db = iegut_db()

        # Šī rinda izpilda parametrizētu SELECT vaicājumu pēc lietotāja ID.
        rinda = db.execute(
            "SELECT id, lietotajvards, vards, parole_hash, loma FROM lietotaji WHERE id = ?",
            (lietotaja_id,)
        ).fetchone()

        # Šī rinda pārvērš DB rindu par Lietotajs objektu.
        return Lietotajs.no_db_rindas(rinda)
