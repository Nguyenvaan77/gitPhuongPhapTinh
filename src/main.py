import numpy as np
from data import get_sample_data, get_random_data, get_sin_data, get_f_data, f
from plot import plot_spline, plot_function, plot_squared_error, plot_absolute_error
from spline import natural_cubic_spline
# from spline_gauss import natural_cubic_spline_gauss

def main():
    x, y = get_f_data()

    a, b, c, d = natural_cubic_spline(x, y)
    # a, b, c, d = spline_gauss(x, y)

    # Vẽ spline tự nhiên
    plot_spline(x, y, a, b, c, d)

    # Vẽ hàm f(x) từ x = -10 đến 10 và số điểm làm mượt là 100
    plot_function(f, -10 , 10 ,num_points=100)

    # Vẽ sai số tuyệt đối
    plot_absolute_error(f, x, a, b, c, d, num_points=500,)

    #Vẽ sai số bình phương
    plot_squared_error(f, x, a, b, c, d, num_points=500)


if __name__ == '__main__':
    main()