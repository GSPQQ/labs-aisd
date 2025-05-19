import math
import timeit
import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def F_rec(n):
    if n < 3:
        return 3
    elif 3 < n <= 25:
        return F_rec(n - 1)
    else:
        sign = -1 if n % 2 == 0 else 1
        return sign * (5 * F_rec(n - 1) / math.factorial(2 * n) - 2 * (n - 2))

def F_iter(n):
    if n < 3:
        return 3
    f_prev = 3
    current_fact = 1  
    for i in range(3, n + 1):
        if 3 < i <= 25:
            f_current = f_prev
        else:
            sign = -1 if i % 2 == 0 else 1
            fact = 1
            for j in range(1, 2*i + 1):
                fact *= j
            f_current = sign * (5 * f_prev) / fact - 2 * (i - 2)
        f_prev = f_current
    return f_prev

def show_graph(results):
    graph_window = tk.Toplevel(root)
    graph_window.title("График времени выполнения")
    graph_window.geometry("800x600")
    
    fig = Figure(figsize=(8, 6), dpi=100)
    plot = fig.add_subplot(111)
    
    plot.plot(results['n'], results['time_rec'], 'r-', label='Рекурсия')
    plot.plot(results['n'], results['time_iter'], 'b-', label='Итерация')
    plot.set_title('Сравнение времени выполнения рекурсивного и итерационного подходов')
    plot.set_xlabel('n')
    plot.set_ylabel('Время (мс)')
    plot.legend()
    plot.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    close_button = ttk.Button(graph_window, text="Закрыть", command=graph_window.destroy)
    close_button.pack(side=tk.BOTTOM, pady=10)
    
    center_window(graph_window)

def calculate():
    try:
        n = int(entry.get())
        if n <= 0:
            raise ValueError
        
        output_text.delete(1.0, tk.END)
        results = {
            'n': [],
            'F_rec': [],
            'F_iter': [],
            'time_rec': [],
            'time_iter': []
        }
        
        output_text.insert(tk.END, f"{'n':<5}{'F рекурсивно':<20}{'F итерационно':<20}{'Время рекурсии (мс)':<20}{'Время итерации (мс)':<20}\n")
        output_text.insert(tk.END, "-"*85 + "\n")
        
        for i in range(1, n + 1):
            start = timeit.default_timer()
            f_rec = F_rec(i)
            time_rec = (timeit.default_timer() - start) * 1000
            
            start = timeit.default_timer()
            f_iter = F_iter(i)
            time_iter = (timeit.default_timer() - start) * 1000
            
            results['n'].append(i)
            results['F_rec'].append(f_rec)
            results['F_iter'].append(f_iter)
            results['time_rec'].append(time_rec)
            results['time_iter'].append(time_iter)
            
            output_text.insert(tk.END, 
                f"{i:<5}"
                f"{f_rec:<20.6f}"
                f"{f_iter:<20.6f}"
                f"{time_rec:<20.4f}"
                f"{time_iter:<20.4f}\n")
            
            root.update()
        
        graph_button.config(state=tk.NORMAL, command=lambda: show_graph(results))
    
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка! Пожалуйста, введите натуральное число больше 0.")
        graph_button.config(state=tk.DISABLED)

# Основное окно
root = tk.Tk()
root.title("Вычисление функции F(n)")
root.geometry("800x600")

# Центрируем главное окно
root.withdraw()  # Скрываем окно перед центрированием
root.after(0, lambda: center_window(root))
root.deiconify()  # Показываем окно после центрирования

# Фрейм для ввода
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X)

# Элементы ввода
ttk.Label(input_frame, text="Введите натуральное число N:").pack(side=tk.LEFT, padx=5)
entry = ttk.Entry(input_frame, width=10)
entry.pack(side=tk.LEFT, padx=5)

# Кнопки
button_frame = ttk.Frame(input_frame)
button_frame.pack(side=tk.LEFT, padx=10)

calculate_btn = ttk.Button(button_frame, text="Рассчитать", command=calculate)
calculate_btn.pack(side=tk.LEFT, padx=5)

graph_button = ttk.Button(button_frame, text="Показать график", state=tk.DISABLED)
graph_button.pack(side=tk.LEFT, padx=5)

# Фрейм для вывода
output_frame = ttk.Frame(root, padding="10")
output_frame.pack(fill=tk.BOTH, expand=True)

# Текстовое поле с прокруткой
output_text = scrolledtext.ScrolledText(output_frame, width=100, height=25, wrap=tk.NONE)
output_text.pack(fill=tk.BOTH, expand=True)

# Горизонтальная прокрутка
x_scroll = ttk.Scrollbar(output_frame, orient=tk.HORIZONTAL, command=output_text.xview)
x_scroll.pack(fill=tk.X)
output_text.configure(xscrollcommand=x_scroll.set)

root.mainloop()