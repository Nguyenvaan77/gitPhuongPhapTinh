import numpy as np

def natural_cubic_spline(x, y):
    n = len(x) - 1
    h = [x[i+1] - x[i] for i in range(n)]

    A = np.zeros((n+1, n+1))
    B = np.zeros(n+1, 1)

    A[0][0] = 1
    A[n][n] = 1
    B[0][0] = 0
    B[n][0] = 0

    for i in range(1,n):
        A[i][i - 1] = h[i -1]
        A[i][i] = 2 * (h[i - 1] + h[i])
        A[i][i + 1] = h[i]
        B[i][0] = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i -1 ]) / h[i - 1])

        c = gauss_elimination(A, B)

        a = [y[i] for i in range(n)]
        b = [(y[i + 1] - y[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3 for i in range(n)]
        d = [(c[i + 1] - c[i]) / (3 * h[i]) for i in range(n)]

        return a, b, c[:-1], d

def gauss_elimination(a_matrix, b_matrix):
    a = a_matrix.astype(float).copy()
    b = b_matrix.astype(float).flatten()
    n = len(b)

    for i in range(n):
        max_row = i + np.argmax(abs(a[i:, i]))
        if abs(a[max_row, i]) < 1e-12:
            raise ValueError("Pivot gần 0 → hệ phương trình vô nghiệm hoặc vô số nghiệm")

        if max_row != i:
            a[[i, max_row]] = a[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]

        for j in range(i + 1, n):
            ratio = a[j, i] / a[i, i]
            a[j, i:] -= ratio * a[i, i:]
            b[j] -= ratio * b[i]

    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (b[i] - np.dot(a[i, i+1:], x[i+1:])) / a[i, i]

    return x

A = np.array([[2, -1, 1],
              [3, 3, 9],
              [3, 3, 5]], dtype=float)
b = np.array([[2], [-1], [4]], dtype=float)

x = gauss_elimination(A, b)
print("Nghiệm x:", x)
