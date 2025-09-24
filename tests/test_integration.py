import pytest
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_log_form(client):
    response = client.get('/log')
    assert b'Log Activity' in response.data


def test_summary_displays_activity_resume(client):
    """
    Vérifie l'affichage d'un résumé des activités.
    Le test passe si :
      - une des routes candidates répond 200
      - et que le contenu contient 'summary' ou 'resume'
        ET 'activity' ou 'activit'
    """
    candidates = ["/summary", "/activities/summary", "/resume", "/"]
    ok = False
    for path in candidates:
        resp = client.get(path)
        if resp.status_code == 200:
            body = resp.get_data(as_text=True)
            normalized = (
                body.lower()
                .replace("é", "e").replace("è", "e").replace("ê", "e")
                .replace("à", "a").replace("â", "a")
            )
            if (("summary" in normalized or "resume" in normalized)
                and ("activity" in normalized or "activit" in normalized)):
                ok = True
                break
    assert ok, "Aucune page de résumé trouvée ou contenu de résumé absent."
