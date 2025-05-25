# main.py
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from ttkthemes import ThemedTk
from plot import plot_spline # plot_spline vẫn cần để vẽ Figure
from gui_app import SplineAppGUI
from core_logic import calculate_plot_data_core, calculate_single_point_details_core # << IMPORT TỪ CORE_LOGIC

# Các biến toàn cục cho logic
canvas_tk_widget = None
toolbar_tk_widget = None
current_spline_coeffs_tuple_main = None 
current_x_nodes_main = None

app_ui = None

def run_logic():
    global canvas_tk_widget, toolbar_tk_widget
    global current_spline_coeffs_tuple_main, current_x_nodes_main 
    global app_ui

    if app_ui is None:
        print("Lỗi: app_ui chưa được khởi tạo.")
        return

    app_ui.update_interpolation_results("---", "---", "---")
    current_spline_coeffs_tuple_main = None
    current_x_nodes_main = None

    try:
        inputs = app_ui.get_input_values()
        expr_str_raw = inputs["expr"]
        n_nodes_str = inputs["n_nodes"]
        a_val_str = inputs["a_val"]
        b_val_str = inputs["b_val"]

        if not expr_str_raw:
            messagebox.showerror("Lỗi", "Vui lòng nhập hàm f(x).")
            return
        if not n_nodes_str or not a_val_str or not b_val_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ số điểm (n), khoảng a và b.")
            return

        try:
            n_nodes = int(n_nodes_str)
            a_val = float(a_val_str)
            b_val = float(b_val_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Số điểm (n), a, b phải là số hợp lệ.")
            return

        if n_nodes <= 1:
            messagebox.showerror("Lỗi", "Số điểm nút (n) phải lớn hơn 1.")
            return
        if a_val >= b_val:
            messagebox.showerror("Lỗi", "Giá trị 'a' phải nhỏ hơn 'b'.")
            return

        # Gọi hàm từ core_logic để thực hiện tính toán
        plot_data = calculate_plot_data_core(expr_str_raw, n_nodes, a_val, b_val)

        # Lưu lại kết quả cần thiết để nội suy điểm
        current_x_nodes_main = plot_data["x_nodes"]
        current_spline_coeffs_tuple_main = plot_data["current_spline_coeffs_tuple"]
        
        # Chuẩn bị dữ liệu cho hàm plot_spline của module plot
        fig = plot_spline(
            x_data_points=plot_data["x_nodes"],
            y_data_points=plot_data["y_nodes"],
            coeff_a=plot_data["coeff_a"], # Lấy từ kết quả của core_logic
            coeff_b=plot_data["coeff_b"],
            coeff_c=plot_data["coeff_c"],
            coeff_d=plot_data["coeff_d"],
            x_original_dense=plot_data["x_original_dense"],
            y_original_dense=plot_data["y_original_dense"],
            original_func_label=f"f(x): {plot_data['expr_str_raw']}"
        )

        plot_frame_from_gui = app_ui.get_plot_frame()

        if canvas_tk_widget: canvas_tk_widget.destroy()
        if toolbar_tk_widget: toolbar_tk_widget.destroy()
        
        canvas_tk_widget = None 
        toolbar_tk_widget = None

        canvas = FigureCanvasTkAgg(fig, master=plot_frame_from_gui)
        canvas.draw()
        canvas_tk_widget = canvas.get_tk_widget()
        
        toolbar = NavigationToolbar2Tk(canvas, plot_frame_from_gui, pack_toolbar=False)
        toolbar.update()
        toolbar_tk_widget = toolbar
        
        toolbar_tk_widget.pack(side=tk.BOTTOM, fill=tk.X)
        canvas_tk_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    except ValueError as ve: 
        messagebox.showerror("Lỗi Dữ Liệu hoặc Tính Toán", str(ve))
        current_spline_coeffs_tuple_main = None
        current_x_nodes_main = None
    except ZeroDivisionError:
        messagebox.showerror("Lỗi Tính Toán", "Lỗi chia cho không. Kiểm tra lại hàm và khoảng giá trị.")
        current_spline_coeffs_tuple_main = None
        current_x_nodes_main = None
    except Exception as e:
        messagebox.showerror("Lỗi Thực Thi", f"Lỗi không mong muốn trong run_logic: {str(e)}")
        current_spline_coeffs_tuple_main = None
        current_x_nodes_main = None
        import traceback
        traceback.print_exc()


def interpolate_logic():
    global current_spline_coeffs_tuple_main, current_x_nodes_main
    global app_ui

    if app_ui is None:
        print("Lỗi: app_ui chưa được khởi tạo cho nội suy.")
        return

    app_ui.update_interpolation_results(y_spline_text="---", y_original_text="---", error_text="---")

    if current_spline_coeffs_tuple_main is None or current_x_nodes_main is None:
        messagebox.showinfo("Thông báo", "Vui lòng vẽ đồ thị spline trước để có dữ liệu nội suy.")
        return
    
    y_spline_text_ui = "---"
    y_original_text_ui = "---"
    error_text_ui = "---"

    try:
        x_query_str = app_ui.get_interpolate_x_value()
        if not x_query_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị x để nội suy.")
        else:
            x_query = float(x_query_str)
            
            # Lấy lại biểu thức hàm f(x) từ UI để tính giá trị gốc
            inputs_for_f_x = app_ui.get_input_values()
            expr_str_for_f_x = inputs_for_f_x["expr"]

            results = calculate_single_point_details_core(
                x_query,
                current_x_nodes_main,
                current_spline_coeffs_tuple_main,
                expr_str_for_f_x
            )

            if results["y_spline_result"] is not None:
                y_spline_text_ui = f"{results['y_spline_result']:.7g}"
            else:
                min_x_node, max_x_node = np.min(current_x_nodes_main), np.max(current_x_nodes_main)
                msg_extra = ""
                if x_query < min_x_node or x_query > max_x_node:
                    msg_extra = " (Ngoài khoảng dữ liệu)"
                y_spline_text_ui = f"Không thể tính{msg_extra}"

            # Xử lý y_original và error (có thể là số hoặc chuỗi báo lỗi/trạng thái)
            if isinstance(results["y_original_result"], (int, float, np.number)):
                y_original_text_ui = f"{results['y_original_result']:.7g}"
            elif results["y_original_result"] is not None: # Là chuỗi thông báo
                y_original_text_ui = str(results["y_original_result"])
            # else y_original_text_ui vẫn là "---"

            if isinstance(results["error_value"], (int, float, np.number)):
                error_text_ui = f"{results['error_value']:.6e}"
            elif results["error_value"] is not None: # Là chuỗi thông báo
                error_text_ui = str(results["error_value"])
            elif results["y_spline_result"] is not None and y_original_text_ui not in ["---", "Chưa nhập f(x)", "Lỗi tính f(x)", "f(x) không hợp lệ", "Lỗi ngoại lệ f(x)"]:
                # Trường hợp này xảy ra nếu y_original_result là None nhưng không phải do lỗi rõ ràng
                error_text_ui = "Không thể tính sai số"


    except ValueError: # Lỗi từ float(x_query_str)
        messagebox.showerror("Lỗi", "Giá trị x nhập vào phải là một số.")
        y_spline_text_ui = "Lỗi x" 
    except NameError:
        messagebox.showerror("Lỗi", "Thành phần giao diện nội suy chưa sẵn sàng.")
    except Exception as e:
        messagebox.showerror("Lỗi Nội Suy", f"Lỗi không mong muốn: {str(e)}")
        y_spline_text_ui = "Lỗi"
        y_original_text_ui = "Lỗi"
        error_text_ui = "Lỗi"
        import traceback
        traceback.print_exc()
    
    app_ui.update_interpolation_results(y_spline_text_ui, y_original_text_ui, error_text_ui)

plot_frame = ttk.LabelFrame(main_frame, text="Đồ thị Spline", padding="10")
plot_frame.pack(pady=(0,10), padx=5, fill='both', expand=True)
window.mainloop()

if __name__ == '__main__':
    root = ThemedTk(theme="adapta") 
    
    app_ui = SplineAppGUI(root, run_command_callback=run_logic, interpolate_command_callback=interpolate_logic)
    
    root.mainloop()
