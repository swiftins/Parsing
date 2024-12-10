import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

def select_file():
    filepath = filedialog.askopenfilename(
        title="Выберите PDF файл",
        filetypes=[("PDF файлы", "*.pdf")]
    )
    if filepath:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, filepath)

def save_shortened_pdf():
    try:
        filepath = entry_file_path.get()
        start_page = int(entry_start_page.get()) - 1  # Нумерация страниц начинается с 0
        end_page = int(entry_end_page.get())
        
        reader = PdfReader(filepath)
        writer = PdfWriter()

        if start_page < 0 or end_page > len(reader.pages) or start_page >= end_page:
            messagebox.showerror("Ошибка", "Некорректный диапазон страниц.")
            return
        
        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])

        save_filepath = filedialog.asksaveasfilename(
            title="Сохранить укороченный PDF",
            defaultextension=".pdf",
            filetypes=[("PDF файлы", "*.pdf")]
        )
        if save_filepath:
            with open(save_filepath, "wb") as output_file:
                writer.write(output_file)
            messagebox.showinfo("Успех", "PDF документ успешно сохранён!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

# Создание основного окна
root = tk.Tk()
root.title("PDF Укоротитель")

# Поле для выбора файла
frame_file = tk.Frame(root)
frame_file.pack(pady=10)
btn_select_file = tk.Button(frame_file, text="Выбрать файл", command=select_file)
btn_select_file.pack(side=tk.LEFT, padx=5)
entry_file_path = tk.Entry(frame_file, width=50)
entry_file_path.pack(side=tk.LEFT, padx=5)

# Поля для ввода диапазона страниц
frame_range = tk.Frame(root)
frame_range.pack(pady=10)
tk.Label(frame_range, text="Начальная страница:").pack(side=tk.LEFT, padx=5)
entry_start_page = tk.Entry(frame_range, width=5)
entry_start_page.pack(side=tk.LEFT, padx=5)
tk.Label(frame_range, text="Конечная страница:").pack(side=tk.LEFT, padx=5)
entry_end_page = tk.Entry(frame_range, width=5)
entry_end_page.pack(side=tk.LEFT, padx=5)

# Кнопка для сохранения укороченного PDF
btn_save = tk.Button(root, text="Сохранить укороченный PDF", command=save_shortened_pdf)
btn_save.pack(pady=10)

# Запуск приложения
root.mainloop()
