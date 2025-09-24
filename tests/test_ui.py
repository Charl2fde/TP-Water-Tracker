# tests/test_ui.py
# check_env.py
import sys
print(f"Python qui exécute ce script : {sys.executable}")
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# URL de l'application à tester
APP_URL = "http://127.0.0.1:5000"


@pytest.fixture
def browser():
    """
    Fixture Pytest pour initialiser et fermer le driver Selenium.
    Cette fonction s'exécutera avant chaque test qui l'utilise.
    """
    # Le mode "no-headless" (avec interface graphique) est le mode par défaut.
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=720,576")
    driver = webdriver.Chrome()
    
    yield driver
    driver.quit()


def test_homepage_title(browser):
    """
    Teste le titre de la page d'accueil de l'application.

    """
    browser.get(APP_URL)
    
    # 2. Attend que la page soit chargée et que le titre soit correct.
    try:
        WebDriverWait(browser, 3).until(
            EC.title_is("Water Tracker")
        )
    except Exception as e:

        pytest.fail(f"Le titre de la page n'était pas correct dans le temps imparti. Erreur : {e}")

    # 3. Vérifie avec une assertion que le titre de la page est bien celui attendu.
    assert browser.title == "Water Tracker"