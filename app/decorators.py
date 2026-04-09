# Šī rinda importē wraps funkciju dekoratoru veidošanai.
from functools import wraps

# Šī rinda importē abort kļūdas atgriešanai.
from flask import abort

# Šī rinda importē current_user un login_required no Flask-Login.
from flask_login import current_user, login_required

# Šī funkcija izveido dekoratoru lomas pārbaudei.
def loma_prasita(prasita_loma):
    # Šī iekšējā funkcija saņem oriģinālo maršruta funkciju.
    def dekorators(f):
        # Šī rinda saglabā oriģinālās funkcijas nosaukumu un metadatus.
        @wraps(f)
        # Šī rinda nodrošina, ka funkcijai var piekļūt tikai pieslēdzies lietotājs.
        @login_required
        # Šī iekšējā funkcija izpilda lomas pārbaudi.
        def ietinamais(*args, **kwargs):
            # Šī rinda pārbauda, vai lietotāja loma sakrīt ar prasīto lomu.
            if current_user.loma != prasita_loma:
                # Šī rinda pārtrauc izpildi un atgriež 403 Forbidden kļūdu.
                abort(403)

            # Šī rinda izsauc oriģinālo funkciju, ja loma ir pareiza.
            return f(*args, **kwargs)

        # Šī rinda atgriež ietīto funkciju.
        return ietinamais

    # Šī rinda atgriež pašu dekoratoru.
    return dekorators
