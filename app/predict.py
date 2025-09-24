import numpy as np

def predict_water(sleeptime=None, steps=None):
    if sleeptime is None and steps is None:
        return None
    return 0.002 * np.average(sleeptime) + 0.009 * np.average(steps)