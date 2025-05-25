import numpy as np
import re

def preprocess_expression(expr):
    """
    Tiền xử lý chuỗi biểu thức toán học để chuẩn bị cho việc đánh giá.
    Ưu tiên xử lý các dạng e^... trước khi thay thế chung ^ bằng **.
    """
    expr = expr.lower() # Chuyển thành chữ thường

    # 1. Xử lý các mẫu e^... cụ thể TRƯỚC KHI thay thế chung '^'
    # Ưu tiên các biểu thức có dấu ngoặc đơn rõ ràng e^(biểu_thức_phức_tạp)
    expr = re.sub(r'e\^\((.*?)\)', r'exp(\1)', expr)

    # Xử lý các trường hợp e^biến_đơn_giản hoặc e^số (ví dụ: e^x, e^myvar, e^2, e^3.14)
    # Regex này tìm 'e^' theo sau bởi một tên biến (chữ cái/số/_) hoặc một con số.
    # Tên biến: [a-z_]\w* (bắt đầu bằng chữ cái hoặc _, theo sau bởi chữ, số, hoặc _)
    # Số: \d*\.?\d+ (ví dụ: 2, 2.0, .5, 0.5)
    expr = re.sub(r'e\^([a-z_]\w*|\d*\.?\d+)', r'exp(\1)', expr)

    # 2. Thay thế toán tử lũy thừa chung '^' bằng '**' của Python
    expr = expr.replace('^', '**')

    # 3. Các thay thế hàm chuẩn và hằng số
    replacements = {
        'exp(': 'np.exp(',       # Cho trường hợp người dùng gõ exp() trực tiếp
        'sin(': 'np.sin(',
        'cos(': 'np.cos(',
        'tan(': 'np.tan(',
        'sqrt(': 'np.sqrt(',
        'log10(': 'np.log10(',
        'ln(': 'np.log(',        # ln là logarit tự nhiên
        'log(': 'np.log(',       # Mặc định log là logarit tự nhiên nếu không phải log10
        'abs(': 'np.abs(',
        'pi': 'np.pi',
    }

    for old, new in replacements.items():
        expr = expr.replace(old, new)

    # 4. Xử lý hằng số 'e' (số Euler) nếu nó đứng một mình (không phải là e^ hay exp())
    # Sử dụng \b để đảm bảo 'e' là một từ riêng biệt.
    expr = re.sub(r'\b(e)\b', r'np.e', expr)

    return expr

def generate_data(expr_str, n, a_val, b_val, aeval):
    """
    Tạo dữ liệu (x, y) từ biểu thức f(x), khoảng [a, b] và số điểm n.

    Args:
        expr_str (str): Hàm f(x) dưới dạng chuỗi.
        n (int): Số điểm.
        a_val (float): Giá trị a.
        b_val (float): Giá trị b.
        aeval (asteval.Interpreter): Interpreter an toàn.

    Returns:
        tuple[np.ndarray, np.ndarray]: Mảng x và y.
    """
    processed_expr_str = preprocess_expression(expr_str)
    print (f"Biểu thức đã xử lý: {processed_expr_str}")
    x_points = np.linspace(a_val, b_val, n)
    y_points = []

    # Xóa và cập nhật bảng ký hiệu của asteval cho mỗi lần gọi generate_data
    # để đảm bảo môi trường sạch
    aeval.symtable.clear()
    aeval.symtable['np'] = np  # Cho phép sử dụng các hàm numpy như np.sin, np.exp
    aeval.symtable['x'] = None # Biến x sẽ được cập nhật trong vòng lặp

    for val in x_points:
        aeval.symtable['x'] = val # Cập nhật giá trị hiện tại của x
        result = aeval.eval(processed_expr_str) # Đánh giá biểu thức đã xử lý

        if aeval.error: # Kiểm tra lỗi sau khi đánh giá
            # Thu thập tất cả các thông báo lỗi
            error_messages = []
            for error in aeval.error:
                # error.get_error() trả về (error_type, error_message, filename, lineno, line)
                error_messages.append(error.get_error()[1])
            aeval.error_msg = None # Xóa lỗi đã xử lý trong aeval
            aeval.error = []


            raise ValueError(f"Lỗi khi đánh giá biểu thức tại x={val:.4f} cho biểu thức '{processed_expr_str}':\n{'; '.join(error_messages)}")
        y_points.append(result)

    return x_points, np.array(y_points)
