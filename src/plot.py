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


def plot_spline(x_data_points, y_data_points, coeff_a, coeff_b, coeff_c, coeff_d,
                title="So sánh Spline và Đồ thị Gốc",
                x_original_dense=None, y_original_dense=None, # Tham số mới
                original_func_label="Đồ thị gốc f(x)"):       # Tham số mới
    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)

    if not x_data_points.size or not y_data_points.size:
        ax.set_title("Không có dữ liệu điểm nút để vẽ spline")
        return fig

    # Vẽ Đồ thị Gốc (nếu có dữ liệu)
    if x_original_dense is not None and y_original_dense is not None:
        ax.plot(x_original_dense, y_original_dense, label=original_func_label, color='green', linestyle='--', linewidth=1.5, zorder=1)

    # Tạo các điểm x dày đặc để vẽ đường spline mượt mà
    x_min_val = np.min(x_data_points)
    x_max_val = np.max(x_data_points)
    x_dense_spline_plot = np.linspace(x_min_val, x_max_val, 500)

    y_dense_spline_plot = []
    for xi in x_dense_spline_plot:
        val = eval_spline(x_data_points, coeff_a, coeff_b, coeff_c, coeff_d, xi)
        y_dense_spline_plot.append(val)

    # Vẽ đường spline
    ax.plot(x_dense_spline_plot, y_dense_spline_plot, label="Đường Spline nội suy", color='blue', zorder=2)

    # Vẽ các điểm dữ liệu gốc (điểm nút)
    ax.plot(x_data_points, y_data_points, 'o', label="Điểm nút dữ liệu", color='red', markersize=6, zorder=3)

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend() # Hiển thị chú giải cho các đường

    try:
        fig.tight_layout()
    except Exception:
        pass

    return fig
