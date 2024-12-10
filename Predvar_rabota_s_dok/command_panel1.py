import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF

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

def analyze_pdf():
    try:
        filepath = entry_file_path.get()
        if not filepath:
            messagebox.showerror("Ошибка", "Выберите PDF файл.")
            return
        
        selected_tool = combo_tools.get()
        text = ""
        
        if selected_tool == "PyPDF2":
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text()
        
        elif selected_tool == "PyMuPDF":
            pdf = fitz.open(filepath)
            for page in pdf:
                text += page.get_text()
            pdf.close()
        
        else:
            messagebox.showerror("Ошибка", "Неизвестный инструмент анализа.")
            return
        
        # Показать текст в новом окне
        text_window = tk.Toplevel(root)
        text_window.title("Извлечённый текст")
        text_area = tk.Text(text_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        text_area.insert(tk.END, text)
        text_area.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при анализе PDF: {str(e)}")

# Создание основного окна
root = tk.Tk()
root.title("PDF Укоротитель и Анализатор")

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

# Выбор инструмента анализа
frame_tool = tk.Frame(root)
frame_tool.pack(pady=10)
tk.Label(frame_tool, text="Выберите инструмент анализа:").pack(side=tk.LEFT, padx=5)
combo_tools = ttk.Combobox(frame_tool, values=["PyPDF2", "PyMuPDF"], state="readonly")
combo_tools.set("PyPDF2")
combo_tools.pack(side=tk.LEFT, padx=5)

# Кнопки
btn_analyze = tk.Button(root, text="Анализировать текст", command=analyze_pdf)
btn_analyze.pack(pady=5)
btn_save = tk.Button(root, text="Сохранить укороченный PDF", command=save_shortened_pdf)
btn_save.pack(pady=5)

# Запуск приложения
root.mainloop()
