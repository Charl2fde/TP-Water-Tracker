import pytest

pytestmark = pytest.mark.integration  # ce test ne tourne qu'en PR

def test_summary_displays_resume():
    """
    Vérifie que la page ou l'API de résumé des activités renvoie bien un contenu.
    On teste plusieurs routes candidates : /summary, /activities/summary, /resume.
    """
    from app import create_app  # import tardif pour éviter l'init DB au moment de la collecte

    app = create_app()
    app.testing = True

    candidates = ["/summary", "/activities/summary", "/resume"]
    with app.app_context():
        with app.test_client() as client:
            # Chercher une route qui répond 200
            for path in candidates:
                resp = client.get(path)
                if resp.status_code == 200:
                    body = resp.get_data(as_text=True)
                    # Vérifier que le contenu mentionne un résumé ou des activités
                    assert any(
                        word in body.lower() for word in ["resume", "summary", "activite", "activity"]
                    ), f"Le contenu de {path} ne semble pas contenir de résumé."
                    return
            pytest.fail(f"Aucune des routes {candidates} n'a renvoyé 200")

            
