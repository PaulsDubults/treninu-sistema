# Šī rinda importē sys moduli Python ceļa labošanai.
import sys

# Šī rinda importē pathlib Path klasi ceļu veidošanai.
from pathlib import Path

# Šī rinda pievieno projekta saknes mapi Python importu ceļam.
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Šī rinda importē pytest testēšanas rīkam.
import pytest

# Šī rinda importē create_app funkciju no lietotnes.
from app import create_app

# Šī pytest fixture izveido testēšanas klientu.
@pytest.fixture
def client():
    # Šī rinda izveido lietotnes objektu.
    app = create_app()

    # Šī rinda ieslēdz testēšanas režīmu.
    app.config["TESTING"] = True

    # Šī rinda izveido testēšanas klientu.
    with app.test_client() as client:
        # Šī rinda atgriež testēšanas klientu testiem.
        yield client

# Šis tests pārbauda, vai sākumlapa atveras.
def test_sakumlapa(client):
    # Šī rinda pieprasa sākumlapu.
    response = client.get("/")

    # Šī rinda pārbauda, vai statusa kods ir 200.
    assert response.status_code == 200
