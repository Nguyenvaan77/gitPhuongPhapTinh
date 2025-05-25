# gui_app.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
# Các import cần thiết khác cho GUI (nếu có)

class SplineAppGUI:
    def __init__(self, master_window, run_command_callback, interpolate_command_callback):
        self.master = master_window
        self.master.title("Ứng Dụng Phân Tích Spline Bậc Ba") # Tiêu đề rõ ràng hơn
        self.master.geometry("850x820") # Điều chỉnh chiều cao nếu cần

        self.style = ttk.Style(self.master)
        self.style.configure("TLabelFrame.Label", font=("Arial", 13, "bold"))
        self.style.configure("Accent.TButton", font=("Arial", 12, "bold"), padding="5 5")

        # Callback functions từ file main
        self.run_command = run_command_callback
        self.interpolate_command = interpolate_command_callback

        self._create_widgets()

    def _create_widgets(self):
        # --- Khung chính ---
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Cấu hình grid cho main_frame để các phần tử con sắp xếp đúng
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)  # input_outer_frame
        self.main_frame.rowconfigure(1, weight=0)  # control_frame
        self.main_frame.rowconfigure(2, weight=1)  # plot_frame (sẽ co giãn)
        self.main_frame.rowconfigure(3, weight=0)  # interpolate_frame

        # --- Khung Nhập liệu Tham số ---
        # Đảm bảo self.main_frame là tham số đầu tiên
        self.input_outer_frame = ttk.LabelFrame(self.main_frame, text="Tham số đầu vào", padding="10")
        self.input_outer_frame.grid(row=0, column=0, pady=(0,10), padx=5, sticky="ew")

        ttk.Label(self.input_outer_frame, text="Hàm f(x):", font=("Arial", 12)).grid(row=0, column=0, padx=(0,5), pady=8, sticky="w")
        self.entry_func = ttk.Entry(self.input_outer_frame, width=60, font=("Arial", 11))
        self.entry_func.insert(0, "np.sin(x) + 0.5*np.cos(2*x)") # Hàm ví dụ
        self.entry_func.grid(row=0, column=1, columnspan=3, padx=5, pady=8, sticky="ew")

        self.details_frame = ttk.Frame(self.input_outer_frame)
        self.details_frame.grid(row=1, column=0, columnspan=4, pady=(10,5), sticky="ew")

        ttk.Label(self.details_frame, text="Số điểm (n):", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,5))
        self.entry_n = ttk.Entry(self.details_frame, width=10, font=("Arial", 10))
        self.entry_n.insert(0, "15")
        self.entry_n.pack(side=tk.LEFT, padx=(0,20))

        ttk.Label(self.details_frame, text="Khoảng [a, b]", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,10))
        ttk.Label(self.details_frame, text="a:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,5))
        self.entry_a = ttk.Entry(self.details_frame, width=8, font=("Arial", 10))
        self.entry_a.insert(0, "0")
        self.entry_a.pack(side=tk.LEFT, padx=(0,10))

        ttk.Label(self.details_frame, text="b:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,5))
        self.entry_b = ttk.Entry(self.details_frame, width=8, font=("Arial", 10))
        self.entry_b.insert(0, "10")
        self.entry_b.pack(side=tk.LEFT, padx=(0,5))

        self.input_outer_frame.columnconfigure(1, weight=1) # Cho entry_func mở rộng

        # --- Khung Điều khiển ---
        self.control_frame = ttk.Frame(self.main_frame) # Parent là self.main_frame
        self.control_frame.grid(row=1, column=0, pady=5, sticky="ew")
        self.run_button = ttk.Button(self.control_frame, text="Vẽ Đồ Thị", command=self.run_command, style="Accent.TButton", width=18)
        self.run_button.pack(pady=5) # Nút pack bên trong control_frame

        # --- Khung Đồ thị ---
        self.plot_frame = ttk.LabelFrame(self.main_frame, text="Đồ thị So Sánh", padding="10")
        self.plot_frame.grid(row=2, column=0, pady=(0,5), padx=5, sticky="nsew")

        # --- Khung Nội suy & Sai số ---
        self.interpolate_frame = ttk.LabelFrame(self.main_frame, text="Nội suy & Sai số Tại Điểm", padding="10")
        self.interpolate_frame.grid(row=3, column=0, pady=(5,10), padx=5, sticky="ew")

        ttk.Label(self.interpolate_frame, text="Nhập giá trị x:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.entry_x_interpolate = ttk.Entry(self.interpolate_frame, width=15, font=("Arial", 10))
        self.entry_x_interpolate.grid(row=0, column=1, padx=5, pady=3)
        self.interpolate_button = ttk.Button(self.interpolate_frame, text="Tính y & Sai số", command=self.interpolate_command, width=15)
        self.interpolate_button.grid(row=0, column=2, padx=5, pady=3)

        ttk.Label(self.interpolate_frame, text="Giá trị y (Spline):", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.label_y_interpolated = ttk.Label(self.interpolate_frame, text="---", font=("Arial", 11, "bold"), width=25)
        self.label_y_interpolated.grid(row=1, column=1, columnspan=2, padx=5, pady=3, sticky="w")

        ttk.Label(self.interpolate_frame, text="Giá trị y (Hàm gốc):", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.label_y_original_at_query = ttk.Label(self.interpolate_frame, text="---", font=("Arial", 11, "bold"), width=25)
        self.label_y_original_at_query.grid(row=2, column=1, columnspan=2, padx=5, pady=3, sticky="w")

        ttk.Label(self.interpolate_frame, text="Sai số tuyệt đối:", font=("Arial", 11)).grid(row=3, column=0, padx=5, pady=3, sticky="w")
        self.label_error_interpolated = ttk.Label(self.interpolate_frame, text="---", font=("Arial", 11, "bold"), width=25)
        self.label_error_interpolated.grid(row=3, column=1, columnspan=2, padx=5, pady=3, sticky="w")

    def get_input_values(self):
        return {
            "expr": self.entry_func.get(),
            "n_nodes": self.entry_n.get(),
            "a_val": self.entry_a.get(),
            "b_val": self.entry_b.get()
        }

    def get_interpolate_x_value(self):
        return self.entry_x_interpolate.get()

    def update_interpolation_results(self, y_spline_text, y_original_text, error_text):
        # Kiểm tra widget tồn tại trước khi config để tránh lỗi nếu GUI chưa hoàn tất tạo
        if hasattr(self, 'label_y_interpolated') and self.label_y_interpolated.winfo_exists():
            self.label_y_interpolated.config(text=y_spline_text)
        if hasattr(self, 'label_y_original_at_query') and self.label_y_original_at_query.winfo_exists():
            self.label_y_original_at_query.config(text=y_original_text)
        if hasattr(self, 'label_error_interpolated') and self.label_error_interpolated.winfo_exists():
            self.label_error_interpolated.config(text=error_text)

    def get_plot_frame(self):
        return self.plot_frame

if __name__ == '__main__':
    # Phần này để test file GUI độc lập nếu cần
    # Bạn cần tạo các hàm lambda đơn giản cho callback để không bị lỗi NameError
    def dummy_run():
        print("Run called from test")

    def dummy_interpolate():
        print("Interpolate called from test")

    root = ThemedTk(theme="adapta")
    app_gui = SplineAppGUI(root, run_command_callback=dummy_run, interpolate_command_callback=dummy_interpolate)
    root.mainloop()