import numpy as np
import matplotlib.pyplot as plt

from spline import eval_spline


def compute_absolute_error(f, x_data, a, b, c, d, num_points=500):
    """
    Tính sai số tuyệt đối |f(x) - S(x)| trên dải từ min đến max của x_data,
    với num_points điểm kiểm tra.

    Trả về:
      x_vals: mảng điểm lấy mẫu
      errors: mảng sai số tương ứng
    """
    x_vals = np.linspace(min(x_data), max(x_data), num_points)
    errors = []
    for x in x_vals:
        s_val = eval_spline(x_data, a, b, c, d, x)
        if s_val is None:
            errors.append(np.nan)  # hoặc bạn có thể skip
        else:
            errors.append(abs(f(x) - s_val))
    return x_vals, errors

# tính sai số bình phương
def compute_squared_error(f, x_data, a, b, c, d, num_points=500):
    """
    Tính sai số bình phương (f(x) - S(x))^2 trên dải từ min đến max của x_data,
    với num_points điểm kiểm tra.

    Trả về:
      x_vals: mảng điểm lấy mẫu
      errors: mảng sai số bình phương tương ứng
    """
    x_vals = np.linspace(min(x_data), max(x_data), num_points)
    errors = []
    for x in x_vals:
        s_val = eval_spline(x_data, a, b, c, d, x)
        if s_val is None:
            errors.append(np.nan)
        else:
            errors.append((f(x) - s_val)**2)
    return x_vals, errors

#Tính sai số tối đa
def compute_max_error(f, x_data, a, b, c, d, num_points=500):
    """
    Tính sai số tuyệt đối |f(x) - S(x)| trên dải từ min đến max của x_data,
    với num_points điểm kiểm tra.

    Trả về:
      max_error: giá trị sai số lớn nhất
      x_max_errors: list các điểm x có sai số lớn nhất
    """
    x_vals = np.linspace(min(x_data), max(x_data), num_points)
    abs_errors = []
    for x in x_vals:
        s_val = eval_spline(x_data, a, b, c, d, x)
        if s_val is None:
            abs_errors.append(np.nan)
        else:
            abs_errors.append(abs(f(x) - s_val))

    abs_errors = np.array(abs_errors)
    max_error = np.nanmax(abs_errors)  # giá trị sai số lớn nhất
    # Tìm tất cả các điểm x có sai số bằng max_error (cho phép sai số số học nhỏ)
    tolerance = 1e-12
    indices = np.where(np.abs(abs_errors - max_error) < tolerance)[0]
    x_max_errors = x_vals[indices].tolist()

    return max_error, x_max_errors

# Tính sai số trung bình
def compute_mae(f, x_data, a, b, c, d, num_points=500):
    """
    Tính trung bình sai số tuyệt đối (MAE) giữa f và spline S trên dải từ min đến max của x_data.
    
    Tham số:
    - f: hàm gốc (callable)
    - x_data: mảng hoặc list điểm mốc spline
    - a, b, c, d: hệ số spline từng đoạn
    - num_points: số điểm lấy mẫu để tính sai số
    
    Trả về:
    - mae: giá trị trung bình sai số tuyệt đối
    """
    x_vals = np.linspace(min(x_data), max(x_data), num_points)
    errors = []
    for x in x_vals:
        s_val = eval_spline(x_data, a, b, c, d, x)
        if s_val is None:
            continue  # bỏ qua điểm ngoài miền
        errors.append(abs(f(x) - s_val))
    mae = np.mean(errors)
    return mae
