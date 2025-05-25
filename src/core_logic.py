# core_logic.py
import numpy as np
from asteval import Interpreter

# Import các hàm cần thiết từ các module khác của bạn
from data import generate_data, preprocess_expression
from spline import natural_cubic_spline
from plot import eval_spline # eval_spline được dùng để tính giá trị spline

def setup_aeval_interpreter():
    """Khởi tạo và cấu hình một đối tượng Aeval Interpreter."""
    aeval = Interpreter()
    aeval.symtable.clear()
    aeval.symtable['np'] = np
    aeval.symtable['x'] = None
    return aeval

def calculate_plot_data_core(expr_str_raw, n_nodes, a_val, b_val):
    """
    Thực hiện các tính toán cốt lõi để lấy dữ liệu cho việc vẽ đồ thị.
    Bao gồm dữ liệu nút, hệ số spline, và dữ liệu cho hàm gốc.
    Trả về một dictionary chứa tất cả các kết quả.
    """
    aeval = setup_aeval_interpreter()

    # 1. Tạo dữ liệu cho các điểm nút của Spline
    x_nodes, y_nodes = generate_data(expr_str_raw, n_nodes, a_val, b_val, aeval)

    # 2. Tính toán các hệ số của Spline
    coeff_a, coeff_b, coeff_c, coeff_d = natural_cubic_spline(x_nodes, y_nodes)

    # 3. Tạo dữ liệu để vẽ đồ thị gốc f(x) một cách mượt mà
    n_points_for_original_func = 500
    x_original_dense = np.linspace(a_val, b_val, n_points_for_original_func)
    y_original_dense_list = [] # Sử dụng list trước rồi chuyển sang array
    processed_expr = preprocess_expression(expr_str_raw)

    for x_val_loop in x_original_dense:
        aeval.symtable['x'] = x_val_loop
        try:
            y_val_loop = aeval.eval(processed_expr)
            if aeval.error:
                y_original_dense_list.append(np.nan)
                aeval.error = [] # Xóa lỗi đã xử lý
                aeval.error_msg = None
                continue
            y_original_dense_list.append(y_val_loop)
        except Exception:
            y_original_dense_list.append(np.nan)
    
    y_original_dense_array = np.array(y_original_dense_list)

    return {
        "x_nodes": x_nodes,
        "y_nodes": y_nodes,
        "coeff_a": coeff_a,
        "coeff_b": coeff_b,
        "coeff_c": coeff_c,
        "coeff_d": coeff_d,
        "current_spline_coeffs_tuple": (coeff_a, coeff_b, coeff_c, coeff_d), # Để tiện dùng
        "x_original_dense": x_original_dense,
        "y_original_dense": y_original_dense_array,
        "expr_str_raw": expr_str_raw # Trả lại để dùng cho nhãn đồ thị
    }

def calculate_single_point_details_core(x_query, current_x_nodes, current_spline_coeffs_tuple, expr_str_raw_for_f_x):
    """
    Tính giá trị spline, giá trị hàm gốc và sai số tại một điểm x_query.
    Trả về một dictionary chứa các giá trị này.
    """
    y_spline = None
    y_original = None # Có thể là số, None, hoặc chuỗi báo lỗi
    error = None    # Có thể là số hoặc None

    # 1. Tính giá trị y từ Spline
    if current_x_nodes is not None and current_spline_coeffs_tuple is not None:
        coeff_a_s, coeff_b_s, coeff_c_s, coeff_d_s = current_spline_coeffs_tuple
        y_spline = eval_spline(current_x_nodes, coeff_a_s, coeff_b_s, coeff_c_s, coeff_d_s, x_query)

    # 2. Tính giá trị y từ hàm gốc f(x) tại x_query (nếu có thể)
    if y_spline is not None: # Chỉ tính f(x) và sai số nếu có giá trị spline
        if not expr_str_raw_for_f_x:
            y_original = "Chưa nhập f(x)" # Thông báo trạng thái
        else:
            try:
                processed_expr_for_error = preprocess_expression(expr_str_raw_for_f_x)
                aeval_local = setup_aeval_interpreter() # Interpreter cục bộ, an toàn
                aeval_local.symtable['x'] = x_query
                temp_y_original = aeval_local.eval(processed_expr_for_error)

                if aeval_local.error:
                    y_original = "Lỗi tính f(x)"
                    # print(f"Lỗi asteval khi tính f(x) cho sai số: {aeval_local.error[0].get_error()[1]}")
                    aeval_local.error = []
                    aeval_local.error_msg = None
                elif isinstance(temp_y_original, (int, float, np.number)):
                    y_original = temp_y_original
                    # 3. Tính sai số tuyệt đối
                    error = abs(y_original - y_spline)
                else:
                    y_original = "f(x) không hợp lệ"
            except Exception as e:
                # print(f"Ngoại lệ khi tính f(x) cho sai số: {e}")
                y_original = "Lỗi ngoại lệ f(x)"
    
    return {
        "y_spline_result": y_spline,
        "y_original_result": y_original, # Đây có thể là số hoặc chuỗi
        "error_value": error
    }