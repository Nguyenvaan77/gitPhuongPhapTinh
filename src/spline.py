def natural_cubic_spline(x, y):
    n = len(x) - 1
    a = y.copy()

    # Step 1:
    h = [x[i + 1] - x[i] for i in range(n)]

    # Step 2:
    alpha = [0] * (n+1)
    for i in range(n):
        alpha[i] = (3 / h[i]) * (a[i + 1] - a[i]) - (3 / h[i - 1]) * (a[i] - a[i - 1])

    # Step 3:
    l = [1] + [0]*n
    mu = [0]*(n+1)
    z = [0]*(n+1)

    # Step 4:
    for i in range(1, n):
        l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1] * z[i - 1]) / l[i]

    # Step 5:
    l[n] = 1
    z[n] = 0
    c = [0]*(n+1)
    b = [0]*n
    d = [0]*n

    # Step 6:
    for j in reversed(range(n)):
        c[j] = z[j] - mu[j]*c[j+1]
        b[j] = (a[j+1] - a[j]) / h[j] - h[j]*(c[j+1] + 2*c[j])/3
        d[j] = (c[j+1] - c[j]) / (3*h[j])

    return a[:-1], b, c[:-1], d


def eval_spline(x_data, a, b, c, d, x_query):
    n = len(a)
    for i in range(n):
        if x_data[i] <= x_query <= x_data[i+1]:
            dx = x_query - x_data[i]
            return a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3
    return None  # nếu x_query nằm ngoài miền