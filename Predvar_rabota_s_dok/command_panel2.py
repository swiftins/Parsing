import tkinter as tk
from tkinter import ttk, messagebox

def Pusk():
    # Получаем введённое имя файла и выбранный метод обработки
    file_name = entry_file_name.get()
    selected_method = combo_methods.get()
    
    # Проверяем, введено ли имя файла и выбран ли метод
    if not file_name:
        messagebox.showerror("Ошибка", "Введите имя файла!")
        return
    if not selected_method:
        messagebox.showerror("Ошибка", "Выберите метод обработки!")
        return
    
    # Выводим информацию о файле и методе обработки
    result_message = f"Имя файла: {file_name}\nМетод обработки: {selected_method}"
    messagebox.showinfo("Информация", result_message)

# Создание основного окна
root = tk.Tk()
root.title("Интерфейс обработки PDF")

# Поле для ввода имени файла
frame_file = tk.Frame(root)
frame_file.pack(pady=10)
tk.Label(frame_file, text="Введите имя файла:").pack(side=tk.LEFT, padx=5)
entry_file_name = tk.Entry(frame_file, width=50)
entry_file_name.pack(side=tk.LEFT, padx=5)

# Выпадающий список для выбора метода обработки
frame_method = tk.Frame(root)
frame_method.pack(pady=10)
tk.Label(frame_method, text="Выберите метод обработки:").pack(side=tk.LEFT, padx=5)
combo_methods = ttk.Combobox(
    frame_method, 
    values=["PyPDF2", "PyMuPDF (fitz)", "pdfplumber", "PyPDF4", "PDFMiner"],
    state="readonly",
    width=20
)
combo_methods.pack(side=tk.LEFT, padx=5)

# Кнопка для запуска программы Pusk
btn_run = tk.Button(root, text="Запуск Pusk", command=Pusk)
btn_run.pack(pady=20)

# Запуск интерфейса
root.mainloop()
