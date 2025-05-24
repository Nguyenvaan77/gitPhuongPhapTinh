from data import get_sample_data, get_random_data
from plot import plot_spline
from spline import natural_cubic_spline
# from spline_gauss import natural_cubic_spline_gauss

def main():
    x, y = get_random_data()

    a, b, c, d = natural_cubic_spline(x, y)
    # a, b, c, d = spline_gauss(x, y)

    plot_spline(x, y, a, b, c, d)

if __name__ == '__main__':
    main()
