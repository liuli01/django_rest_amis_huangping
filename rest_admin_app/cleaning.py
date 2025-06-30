
# yourapp/cleaning.py
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline
import logging
logger = logging.getLogger(__name__)

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



def trend_fit(values, degree=5):
    """
    多项式趋势拟合，返回拟合后的平滑曲线
    :param values: 原始值列表
    :param degree: 多项式拟合阶数（推荐 2~5）
    :return: 拟合后的值列表
    """
    x = np.arange(len(values))
    y = np.array(values)

    # 若数据过短，直接返回原值
    if len(values) < degree + 1:
        return values

    try:
        coeffs = np.polyfit(x, y, deg=degree)
        poly_func = np.poly1d(coeffs)
        fitted = poly_func(x)
        return fitted.tolist()
    except Exception as e:
        logger.error(f"[trend_fit] 拟合失败: {e}")
        return values



def savgol_trend_fit(values, window_length=21, polyorder=2):
    """
    Savitzky-Golay 滤波器进行趋势拟合
    :param values: 原始数据(list)
    :param window_length: 滑动窗口大小（必须为奇数）
    :param polyorder: 多项式阶数（小于窗口大小）
    """
    y = np.array(values)

    # 自动调整窗口长度（数据少时降阶）
    if len(y) < 7:
        return values
    if window_length >= len(y):
        window_length = len(y) - 1 if len(y) % 2 == 0 else len(y)
    if window_length % 2 == 0:
        window_length -= 1
    if polyorder >= window_length:
        polyorder = max(1, window_length - 1)

    try:
        smoothed = savgol_filter(y, window_length=window_length, polyorder=polyorder)
        return smoothed.tolist()
    except Exception as e:
        logger.error(f"[savgol_trend_fit] 拟合失败: {e}")
        return values



def ewma_trend_fit(values, alpha=0.2):
    """
    指数加权移动平均（Exponential Weighted Moving Average）
    alpha 越小越平滑（如 0.1）
    """
    import pandas as pd
    series = pd.Series(values)
    smoothed = series.ewm(alpha=alpha, adjust=False).mean()
    return smoothed.tolist()



def median_then_avg(values, window=5):
    import pandas as pd
    s = pd.Series(values)
    medianed = s.rolling(window=window, center=True, min_periods=3).median()
    smoothed = medianed.rolling(window=window, center=True, min_periods=3).mean()
    return smoothed.tolist()


def lowess_trend_fit(values, frac=0.1):
    """
    frac 越大越平滑，推荐 0.05~0.2
    """

    x = np.arange(len(values))
    y = np.array(values)
    try:
        result = lowess(endog=y, exog=x, frac=frac, return_sorted=False)
        return result.tolist()
    except Exception as e:
        logger.error(f"[lowess_trend_fit] 拟合失败: {e}")
        return values


def spline_trend_fit(values, s=0.5):
    """
    s 越大越平滑；不建议太小（容易震荡）
    """

    x = np.arange(len(values))
    y = np.array(values)
    try:
        spl = UnivariateSpline(x, y, s=s)
        return spl(x).tolist()
    except Exception as e:
        logger.error(f"[spline_trend_fit] 拟合失败: {e}")
        return values

CLEAN_METHODS = {
    "moving_avg": {
        "name": "滑动平均",
        "func": moving_average,
        "describe": "按固定窗口对数据进行平滑处理，适用于趋势平稳的数据"
    },
    "median": {
        "name": "中值滤波",
        "func": median_filter,
        "describe": "通过窗口中值剔除突变异常，适合去除尖刺型噪声"
    },
    "zscore": {
        "name": "Z-Score滤波",
        "func": z_score_filter,
        "describe": "基于标准差判断异常点并剔除，适合高斯型数据"
    },
    "trend_fit": {
        "name": "多项式拟合",
        "func": trend_fit,
        "describe": "使用多项式函数拟合整体趋势，适合平滑波动明显的数据"
    },
    "savgol": {
        "name": "SG滤波",
        "func": savgol_trend_fit,
        "describe": "Savitzky-Golay 滤波器，保留曲线形状的同时平滑波动，适合曲线分析"
    },
    "ewma": {
        "name": "指数加权移动平均",
        "func": ewma_trend_fit,
        "describe": "对较新的数据给予更高权重，适合检测短期趋势"
    },
    "median_avg": {
        "name": "中值+滑动平均组合滤波",
        "func": median_then_avg,
        "describe": "结合中值剔除与滑动平均，适合存在大量异常点的场景"
    },
    "lowess": {
        "name": "LOWESS局部回归拟合",
        "func": lowess_trend_fit,
        "describe": "非参数拟合方法，局部加权回归平滑，适合复杂曲线但效率略低"
    },
    "spline": {
        "name": "三次样条拟合",
        "func": spline_trend_fit,
        "describe": "构造自然平滑曲线，适合较连续、变化不剧烈的趋势拟合"
    }
}
