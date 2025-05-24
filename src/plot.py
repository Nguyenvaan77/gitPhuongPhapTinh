import matplotlib.pyplot as plt
import numpy as np

def eval_spline(x_data, a, b, c, d, x_query):

    n = len(a)
    for i in range(n):
        if x_data[i] <= x_query <= x_data[i+1]:
            dx = x_query - x_data[i]
            return a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3
    return None  # nếu x_query nằm ngoài miền

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
