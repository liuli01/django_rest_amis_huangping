
# yourapp/cleaning.py
import numpy as np
import pandas as pd

def moving_average(values, window=3):
    return pd.Series(values).rolling(window=window, min_periods=10).mean().tolist()

def median_filter(values, window=3):
    return pd.Series(values).rolling(window=window, min_periods=10, center=True).median().tolist()

def z_score_filter(values, threshold=2.0):
    series = pd.Series(values)
    mean = series.mean()
    std = series.std()

    if std == 0 or np.isnan(std):
        # 没有波动，不进行清洗
        return values

    z_scores = (series - mean) / std
    return [v if abs(z) < threshold else None for v, z in zip(series, z_scores)]

CLEAN_METHODS = {
    "moving_avg": {
        "name": "滑动平均",
        "func": moving_average
    },
    "median": {
        "name": "中值滤波",
        "func": median_filter
    },
    "zscore": {
        "name": "Z-Score滤波",
        "func": z_score_filter
    }
}
