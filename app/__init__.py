# Šī rinda importē os moduli darbam ar failu ceļiem.
import os

# Šī rinda importē Flask klasi lietotnes izveidei.
from flask import Flask

# Šī rinda importē LoginManager klasi no Flask-Login bibliotēkas.
from flask_login import LoginManager

# Šī rinda importē pathlib Path klasi ērtākam darbam ar mapēm un failiem.
from pathlib import Path

# Šī rinda izveido LoginManager objektu, kas pārvaldīs lietotāju pieslēgšanos.
login_manager = LoginManager()

# Šī rinda nosaka skata nosaukumu, uz kuru novirzīt neautorizētu lietotāju.
login_manager.login_view = "auth.pieslegties"

# Šī rinda nosaka paziņojuma tekstu, ko Flask-Login var izmantot.
login_manager.login_message = "Lai piekļūtu šai sadaļai, vispirms pieslēdzies."

# Šī rinda nosaka paziņojuma kategoriju dizaina noformējumam.
login_manager.login_message_category = "info"

# Šī funkcija izveido un nokonfigurē Flask lietotni.
def create_app():
    # Šī rinda izveido Flask lietotnes objektu.
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(Path(__file__).resolve().parent.parent / "templates"),
        static_folder=str(Path(__file__).resolve().parent.parent / "static")
    )

    # Šī rinda iestata slepeno atslēgu sesiju parakstīšanai.
    app.config["SECRET_KEY"] = "skolas-projekta-slepena-atslega-2026"

    # Šī rinda iestata ceļu uz SQLite datubāzes failu.
    app.config["DATABASE"] = os.path.join(app.instance_path, "treninu_sistema.db")

    # Šī rinda iestata sīkdatnes HttpOnly režīmu drošībai.
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    # Šī rinda iestata SameSite parametru, lai mazinātu CSRF risku.
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Šī rinda izveido instance mapi, ja tā vēl neeksistē.
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Šī rinda importē DB palīgfunkciju reģistrēšanu.
    from .db import init_app

    # Šī rinda reģistrē DB inicializācijas funkcijas Flask lietotnē.
    init_app(app)

    # Šī rinda piesaista Flask-Login objektu lietotnei.
    login_manager.init_app(app)

    # Šī rinda importē Lietotajs klasi no modeļu faila.
    from .models import Lietotajs

    # Šī dekorētā funkcija pasaka Flask-Login, kā ielādēt lietotāju pēc ID.
    @login_manager.user_loader
    def load_user(user_id):
        # Šī rinda izsauc Lietotajs klases metodi un atgriež lietotāja objektu.
        return Lietotajs.atrast_pec_id(int(user_id))

    # Šī rinda importē autentifikācijas blueprint.
    from .auth import bp as auth_bp

    # Šī rinda importē plāna blueprint.
    from .plans import bp as plans_bp

    # Šī rinda importē rezultātu blueprint.
    from .rezultati import bp as rezultati_bp

    # Šī rinda importē admin blueprint.
    from .admin import bp as admin_bp

    # Šī rinda reģistrē autentifikācijas maršrutus.
    app.register_blueprint(auth_bp)

    # Šī rinda reģistrē plāna maršrutus.
    app.register_blueprint(plans_bp)

    # Šī rinda reģistrē rezultātu maršrutus.
    app.register_blueprint(rezultati_bp)

    # Šī rinda reģistrē admin maršrutus.
    app.register_blueprint(admin_bp)

    # Šī rinda definē sākumlapas maršrutu.
    @app.route("/")
    def index():
        # Šī rinda importē render_template funkciju tikai tur, kur to vajag.
        from flask import render_template

        # Šī rinda atgriež sākumlapas HTML veidni.
        return render_template("index.html")

    # Šī rinda atgriež pilnībā sagatavotu Flask lietotni.
    return app
