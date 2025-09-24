from app.predict import predict_water

def test_predict_water_none():
    assert predict_water() is None
