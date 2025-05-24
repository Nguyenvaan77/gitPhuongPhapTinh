import matplotlib.pyplot as plt
import numpy as np

from error import compute_absolute_error, compute_squared_error
from spline import eval_spline

# Vẽ nội suy spline
def plot_spline(x_data, y_data, a, b, c, d, title="Cubic Spline Interpolation"):

    x_dense = np.linspace(min(x_data), max(x_data), 500)
    y_dense = [eval_spline(x_data, a, b, c, d, xi) for xi in x_dense]

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
    x_vals, errors = compute_absolute_error(f, x_data, a, b, c, d, num_points=num_points)
    mae = np.mean(errors)
    max_err = np.max(errors)
    min_err = np.min(errors)

    plt.figure(figsize=(8,5))
    plt.plot(x_vals[:len(errors)], errors, label="Absolute Error")
    plt.axhline(y=mae, color='r', linestyle='--', label=f'Mean (MAE) = {mae:.4f}')
    plt.axhline(y=max_err, color='g', linestyle=':', label=f'Max = {max_err:.4f}')
    plt.axhline(y=min_err, color='b', linestyle='-.', label=f'Min = {min_err:.4f}')
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("Sai số tuyệt đối")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Vẽ sai số bình phương
def plot_squared_error(f, x_data, a, b, c, d, num_points=500, title="Squared Error of Spline"):
    x_vals, errors = compute_squared_error(f, x_data, a, b, c, d, num_points=num_points)
    mse = np.mean(errors)
    max_err = np.max(errors)
    min_err = np.min(errors)

    plt.figure(figsize=(8,5))
    plt.plot(x_vals[:len(errors)], errors, label="Squared Error")
    plt.axhline(y=mse, color='r', linestyle='--', label=f'Mean (MSE) = {mse:.4f}')
    plt.axhline(y=max_err, color='g', linestyle=':', label=f'Max = {max_err:.4f}')
    plt.axhline(y=min_err, color='b', linestyle='-.', label=f'Min = {min_err:.4f}')
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("Sai số bình phương")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()