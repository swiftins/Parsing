import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

filename = "Крайко А.Н. Краткий курс теоретической газовой динамики. 2007.pdf"
filename = 'ASME Sec II-D-Metric.pdf'

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
