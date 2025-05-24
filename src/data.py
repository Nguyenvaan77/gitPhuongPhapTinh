import numpy as np

def get_sample_data():
    x = [0, 1, 2, 3, 4]
    y = [0, 1, 0, 1, 0]
    return x, y

def get_sin_data():
    x = np.linspace(0, 2 * np.pi, 10)
    y = np.sin(x)
    return list(x), list(y)

def get_random_data():
    try:
        n = int(input("Nhập số điểm ngẫu nhiên muốn tạo (n >= 2): "))
        if n < 2:
            raise ValueError("Phải có ít nhất 2 điểm.")
    except:
        print("Số điểm không hợp lệ, dùng mặc định n = 6.")
        n = 6

    np.random.seed(42)
    x = sorted(np.random.uniform(0, 1000, n))
    y = np.random.uniform(-1000, 1000, n)
    return list(x), list(y)

# Lấy giữ liệu mẫu từ hàm gốc
def get_f_data():
    f = lambda x: x**3 - 3*x**2 + 2
    # Lấy 10 điểm từ -10 đến 10
    x = np.linspace(-4, 4, 20)
    y = f(x)
    return list(x), list(y)

# Hàm gốc
def f(x):
    return x**3 - 3*x**2 + 2
