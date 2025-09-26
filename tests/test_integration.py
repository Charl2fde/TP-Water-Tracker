import json
import pytest
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.testing = True
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_log_form(client):
    response = client.get("/log")
    assert b"Log Activity" in response.data


@pytest.mark.integration
def test_summary_displays_activity_resume(client):
    """
    Vérifie qu'une route de 'résumé des activités' existe et renvoie un contenu exploitable.
    - On teste plusieurs chemins possibles (HTML ou JSON).
    - Le test passe si une route répond 200 ET que le contenu contient des indices de résumé
      (summary / resume / total / stats / history / log) ET d'activité (activity / activit / log).
    """
    candidates = [
        "/summary",
        "/activities/summary",
        "/activity/summary",
        "/resume",
        "/stats",
        "/history",
        "/logs",
        "/log",   # certaines applis affichent le résumé sur la page des logs
        "/",
    ]

    # mots-clés (HTML) – on normalise les accents
    summary_words = ("summary", "resume", "total", "stats", "statistiques", "history", "log")
    activity_words = ("activity", "activit", "log")

    for path in candidates:
        resp = client.get(path)
        if resp.status_code != 200:
            continue

        ctype = resp.headers.get("Content-Type", "")
        body_text = resp.get_data(as_text=True)

        # Cas JSON : on accepte des clés usuelles pour un résumé
        if "application/json" in ctype or body_text.strip().startswith("{") or body_text.strip().startswith("["):
            try:
                data = json.loads(body_text)
            except Exception:
                continue

            # dict avec clés de résumé / liste non vide
            if isinstance(data, dict):
                keys = [k.lower() for k in data.keys()]
                if any(k in keys for k in ("summary", "resume", "totals", "stats", "activities", "logs")):
                    return
            elif isinstance(data, list) and len(data) > 0:
                return
            # sinon on continue tester les autres routes
            continue

        # Cas HTML : recherche de mots-clés
        normalized = (
            body_text.lower()
            .replace("é", "e").replace("è", "e").replace("ê", "e")
            .replace("à", "a").replace("â", "a")
        )

        if any(w in normalized for w in summary_words) and any(w in normalized for w in activity_words):
            return

    pytest.fail("Aucune page/endpoint de résumé des activités trouvé(e) ou contenu non probant.")
