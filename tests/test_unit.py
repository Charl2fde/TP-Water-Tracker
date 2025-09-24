# tests/test_predict.py
import pytest
import numpy as np

from app.predict import predict_water
def test_predict_water_calcul():
    """
    Teste le calcul de la prédiction avec des valeurs d'entrée normales.
    """
    sleeptime_input = [8]
    steps_input = [10000]
    expected_result = 90.016 # 0.002 * 8 + 0.009 * 10000

    result = predict_water(sleeptime=sleeptime_input, steps=steps_input)

    assert result == pytest.approx(expected_result)

def test_predict_water_sans_arguments():
    """
    Teste le cas où la fonction est appelée sans aucun argument.
    Le résultat attendu est None.
    """
    result = predict_water()

    assert result is None

def test_predict_water_autre_calcul():
    """
    Teste le calcul de la prédiction avec un autre jeu de valeurs.
    """
    sleeptime_input = [7]
    steps_input = [5000]
    # Calcul attendu : (0.002 * 7) + (0.009 * 5000) = 0.014 + 45 = 45.014
    expected_result = 45.014

    result = predict_water(sleeptime=sleeptime_input, steps=steps_input)
    
    assert result == pytest.approx(expected_result)

    