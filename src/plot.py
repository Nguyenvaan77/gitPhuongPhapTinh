import matplotlib
try:
    matplotlib.use('TkAgg')
except Exception:
    pass

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

def eval_spline(x_data, a, b, c, d, x_query):
    num_segments = len(a)

    for i in range(num_segments):
        if i + 1 < len(x_data):
            if i == num_segments - 1 and x_query == x_data[i+1]:
                dx = x_query - x_data[i]
                return a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3

            if x_data[i] <= x_query < x_data[i+1]:
                dx = x_query - x_data[i]
                return a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3
        else:
            pass

    if x_query == x_data[num_segments] and num_segments > 0:
        i = num_segments - 1
        dx = x_query - x_data[i]
        return a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3

    return None

def plot_spline(x_data_points, y_data_points, coeff_a, coeff_b, coeff_c, coeff_d, title="Cubic Spline Interpolation"):
    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)

    if not x_data_points.size or not y_data_points.size:
        ax.set_title("Không có dữ liệu để vẽ")
        return fig

    x_min_val = np.min(x_data_points)
    x_max_val = np.max(x_data_points)
    x_dense = np.linspace(x_min_val, x_max_val, 500)

    y_dense_spline = []
    for xi in x_dense:
        val = eval_spline(x_data_points, coeff_a, coeff_b, coeff_c, coeff_d, xi)
        y_dense_spline.append(val)

    ax.plot(x_dense, y_dense_spline, label="Spline Curve", color='blue', zorder=2)
    ax.plot(x_data_points, y_data_points, 'o', label="Data Points", color='red', markersize=5, zorder=3)

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    try:
        fig.tight_layout()
    except Exception:
        pass

    return fig