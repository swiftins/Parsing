import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

filename = "Крайко А.Н. Краткий курс теоретической газовой динамики. 2007.pdf"
#filename = 'ASME Sec II-D-Metric.pdf'

i = int(input('i = '))

if i == 1:
    with open(filename, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        number_of_pages = len(reader.pages)
        print(f"Количество страниц в документе: {number_of_pages}")
elif i == 2:

    with pdfplumber.open(filename) as pdf:
        number_of_pages = len(pdf.pages)
        print(f"Количество страниц в документе: {number_of_pages}")

elif i == 3:

    doc = fitz.open(filename)
    number_of_pages = doc.page_count
    print(f"Количество страниц в документе: {number_of_pages}")
    doc.close()

else:
    with open(filename, "rb") as file:
        parser = PDFParser(file)
        document = PDFDocument(parser)
        number_of_pages = document.num_pages
        print(f"Количество страниц в документе: {number_of_pages}")


### 5. **reportlab**

#Хотя `reportlab` в первую очередь предназначен для создания PDF, его можно использовать для получения количества страниц в процессе создания, 
#о не для анализа существующего PDF. Поэтому он не подходит для этой задачи.

### Выбор библиотеки

#- **PyPDF2** и **pdfplumber** — популярные и простые в использовании для основных задач.
#- **PyMuPDF** предлагает более широкие возможности для манипуляции и анализа PDF-документов.
#- **pdfminer** более сложен, но может быть полезен для извлечения текста и метаданных.


import pandas as pd
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
import pdfplumber
from pdfminer.high_level import extract_pages
from PyPDF4 import PdfFileReader
import time
import os


def count_pages_all_methods(pdf_path):
    results = []

    t0 = time.time()
    # Метод 1: PyPDF2
    try:
        reader = PdfReader(pdf_path)
        l = len(reader.pages)
    except Exception as e:
        print(f"Ошибка в PyPDF2 ({pdf_path}): {e}")
        l = None

    t1 = time.time()
    results.append((l, f'{t1 - t0:.2f}'))

    # Метод 2: PyMuPDF (fitz)
    try:
        doc = fitz.open(pdf_path)
        l = doc.page_count
    except Exception as e:
        print(f"Ошибка в PyMuPDF ({pdf_path}): {e}")
        l = None

    t2 = time.time()
    results.append((l, f'{t2 - t1:.2f}'))
    # Метод 3: pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            l = len(pdf.pages)
    except Exception as e:
        print(f"Ошибка в pdfplumber ({pdf_path}): {e}")
        l = None

    t3 = time.time()
    results.append((l, f'{t3 - t2:.2f}'))
    # Метод 4: PDFMiner
    try:
        print(1/0)
        num_pages = sum(1 for _ in extract_pages(pdf_path))
        l = num_pages
    except Exception as e:
        print(f"Ошибка в PDFMiner ({pdf_path}): {e}")
        l = None

    t4 = time.time()
    results.append((l, f'{t4 - t3:.2f}'))
    # Метод 5: PyPDF4
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfFileReader(f)
            l = reader.numPages
    except Exception as e:
        print(f"Ошибка в PyPDF4 ({pdf_path}): {e}")
        l = None
    t5 = time.time()
    results.append((l, f'{t5 - t4:.2f}'))
    return tuple(results)


# Список PDF файлов

directory = os.getcwd()  # Замените на путь к вашей директории
pdf_files = []
Number_of_pages = []

# Обход директории и вложенных папок
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".pdf"):
            # Добавляем полный путь к файлу в список
#            pdf_files.append(os.path.join(root, file))
            pdf_files.append(file)




# Создание общего списка
results_list = []
for pdf_file in pdf_files:
    page_counts = count_pages_all_methods(pdf_file)
    results_list.append((pdf_file, *page_counts))

# Создание DataFrame
columns = ["File Name", "PyPDF2", "PyMuPDF", "pdfplumber", "PDFMiner", "PyPDF4"]
df = pd.DataFrame(results_list, columns=columns)

# Сохранение DataFrame в CSV (если нужно)
try:
    df.to_csv("pdf_page_counts.csv", index=False, encoding = 'utf-8-sig')
except:
    df.to_csv("pdf_page_counts1.csv", index=False, encoding = 'utf-8-sig')

# Вывод DataFrame
print(df)

