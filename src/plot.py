import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import matplotlib
from error import compute_absolute_error, compute_squared_error
from spline import eval_spline

try:
    matplotlib.use('TkAgg')
except Exception:
    pass
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
    # Vẽ
    plt.figure(figsize=(8, 5))
    plt.plot(x_dense, y_dense, label="Spline Curve", color='blue')
    plt.plot(x_data, y_data, 'ro', label="Data Points")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Vẽ đồ thị hàm gốc
def plot_function(f, x_min, x_max, num_points=500, title="Đồ thị hàm gốc"):
    """
    Vẽ đồ thị hàm số f trong khoảng [x_min, x_max].

    Parameters:
    - f: hàm toán học (callable), nhận đầu vào số hoặc mảng numpy
    - x_min, x_max: khoảng giá trị trục x để vẽ
    - num_points: số điểm dùng để vẽ (mặc định 500)
    - title: tiêu đề đồ thị
    """
    x_vals = np.linspace(x_min, x_max, num_points)
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals, label='Hàm gốc f(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

# Vẽ sai số tuyệt đối
def plot_absolute_error(f, x_data, a, b, c, d, num_points=500, title="Absolute Error of Spline"):
    """
    Vẽ đồ thị sai số tuyệt đối |f(x) - S(x)| trên dải từ min đến max của x_data.
    f: hàm gốc (callable)
    num_points: số điểm lấy mẫu để tính sai số
    """
    x_vals, errors = compute_absolute_error(f, x_data, a, b, c, d, num_points=500)

    plt.figure(figsize=(8,5))
    plt.plot(x_vals[:len(errors)], errors, label="Absolute Error")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("Sai số tuyệt đối")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Vẽ sai số bình phương
def plot_squared_error(f, x_data, a, b, c, d, num_points=500, title="Squared Error of Spline"):
    """
    Vẽ đồ thị sai số bình phương (f(x) - S(x))^2 trên dải từ min đến max của x_data.
    f: hàm gốc (callable)
    num_points: số điểm lấy mẫu để tính sai số
    """
    x_vals, errors = compute_squared_error(f, x_data, a, b, c, d, num_points=num_points)

    plt.figure(figsize=(8,5))
    plt.plot(x_vals[:len(errors)], errors, label="Squared Error")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("Sai số bình phương")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
