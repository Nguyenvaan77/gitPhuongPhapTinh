import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # << IMPORT NavigationToolbar2Tk
from data import generate_data
from spline import natural_cubic_spline
from plot import plot_spline
from asteval import Interpreter
from ttkthemes import ThemedTk

canvas_tk_widget = None # Đổi tên cho rõ ràng hơn (widget của canvas)
toolbar_tk_widget = None # Biến toàn cục cho widget của toolbar

def run():
    global canvas_tk_widget, toolbar_tk_widget # Thêm toolbar_tk_widget vào global
    try:
        expr = entry_func.get()
        n_str = entry_n.get()
        a_str = entry_a.get()
        b_str = entry_b.get()

        if not expr:
            messagebox.showerror("Lỗi", "Vui lòng nhập hàm f(x).")
            return
        if not n_str or not a_str or not b_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ số điểm (n), khoảng a và b.")
            return

        n = int(n_str)
        a_val = float(a_str)
        b_val = float(b_str)

        if n <= 1:
            messagebox.showerror("Lỗi", "Số điểm (n) phải lớn hơn 1.")
            return
        if a_val >= b_val:
            messagebox.showerror("Lỗi", "Giá trị 'a' phải nhỏ hơn 'b'.")
            return

        aeval = Interpreter()
        x, y = generate_data(expr, n, a_val, b_val, aeval)
        aa, bb, cc, dd = natural_cubic_spline(x, y)
        fig = plot_spline(x, y, aa, bb, cc, dd)

        # Xóa canvas và toolbar cũ nếu chúng tồn tại
        if canvas_tk_widget:
            canvas_tk_widget.destroy()
            canvas_tk_widget = None
        if toolbar_tk_widget:
            toolbar_tk_widget.destroy()
            toolbar_tk_widget = None
        
        # Tạo canvas mới
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas_tk_widget = canvas.get_tk_widget()
        
        # Tạo toolbar mới
        # NavigationToolbar2Tk cần tham chiếu đến canvas và frame cha (plot_frame)
        # pack_toolbar=False (nếu dùng) cho phép bạn tự pack toolbar.
        # Trong các phiên bản Matplotlib mới hơn, bạn chỉ cần truyền frame cha.
        toolbar = NavigationToolbar2Tk(canvas, plot_frame, pack_toolbar=False)
        toolbar.update() # Cần thiết để toolbar tự cấu hình
        toolbar_tk_widget = toolbar # Lưu lại tham chiếu đến toolbar (nó là một Frame)
        
        # Đóng gói (pack) toolbar và canvas
        # Toolbar thường ở trên hoặc dưới canvas. Ở đây đặt ở dưới.
        toolbar_tk_widget.pack(side=tk.BOTTOM, fill=tk.X)
        canvas_tk_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    except ValueError as ve:
        messagebox.showerror("Lỗi Dữ Liệu hoặc Tính Toán", str(ve))
    except Exception as e:
        messagebox.showerror("Lỗi Thực Thi", f"Đã xảy ra lỗi không mong muốn: {str(e)}\nKiểm tra lại biểu thức hàm và các giá trị nhập.")
        import traceback
        traceback.print_exc()

# --- Thiết lập GUI ---
window = ThemedTk(theme="adapta")

window.title("Ứng Dụng Vẽ Spline Nội Suy Bậc 3 Tự Nhiên")
window.geometry("850x750")

style = ttk.Style(window)
main_frame = ttk.Frame(window, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

input_outer_frame = ttk.LabelFrame(main_frame, text="Tham số đầu vào", padding="10 10 10 10")
input_outer_frame.pack(pady=(0,10), padx=5, fill='x')

ttk.Label(input_outer_frame, text="Hàm f(x):", font=("Arial", 12)).grid(row=0, column=0, padx=(0,5), pady=8, sticky="w")
entry_func = ttk.Entry(input_outer_frame, width=60, font=("Arial", 11))
entry_func.grid(row=0, column=1, columnspan=3, padx=5, pady=8, sticky="ew")

details_frame = ttk.Frame(input_outer_frame)
details_frame.grid(row=1, column=0, columnspan=4, pady=(10,5), sticky="ew")

ttk.Label(details_frame, text="Số điểm (n):", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,5))
entry_n = ttk.Entry(details_frame, width=10, font=("Arial", 10))
entry_n.insert(0, "20")
entry_n.pack(side=tk.LEFT, padx=(0,20))

ttk.Label(details_frame, text="Khoảng [a, b]", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,10))
ttk.Label(details_frame, text="a:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,5))
entry_a = ttk.Entry(details_frame, width=8, font=("Arial", 10))
entry_a.insert(0, "0")
entry_a.pack(side=tk.LEFT, padx=(0,10))

ttk.Label(details_frame, text="b:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0,5))
entry_b = ttk.Entry(details_frame, width=8, font=("Arial", 10))
entry_b.insert(0, "10")
entry_b.pack(side=tk.LEFT, padx=(0,5))

input_outer_frame.columnconfigure(1, weight=1)

control_frame = ttk.Frame(main_frame)
control_frame.pack(pady=10)

style.configure("Accent.TButton", font=("Arial", 12, "bold"), padding="5 5")
run_button = ttk.Button(control_frame, text="Vẽ Đồ Thị Spline", command=run, style="Accent.TButton", width=20)
run_button.pack(pady=5)

plot_frame = ttk.LabelFrame(main_frame, text="Đồ thị Spline", padding="10")
plot_frame.pack(pady=(0,10), padx=5, fill='both', expand=True)
window.mainloop()