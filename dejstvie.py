import fitz  # PyMuPDF
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
from PyPDF4 import PdfFileReader, PdfFileWriter
from pdfminer.high_level import extract_text

def dejstvie(file_pdf, programma_obrabotki, method_obrabotki):
    try:
        if programma_obrabotki == 1:  # PyPDF2
            if method_obrabotki == 1:  # Извлечь текст
                reader = PdfReader(file_pdf)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                save_result("output_text.txt", text)
            elif method_obrabotki == 4:  # Урезать документ
                writer = PdfWriter()
                reader = PdfReader(file_pdf)
                start_page, end_page = 0, 2  # Пример диапазона страниц
                for i in range(start_page, end_page):
                    writer.add_page(reader.pages[i])
                save_result("output_trimmed.pdf", writer, is_pdf=True)
        
        elif programma_obrabotki == 2:  # PyMuPDF (fitz)
            pdf = fitz.open(file_pdf)
            if method_obrabotki == 1:  # Извлечь текст
                text = ""
                for page in pdf:
                    text += page.get_text()
                save_result("output_text.txt", text)
            elif method_obrabotki == 3:  # Извлечь рисунки
                for page_num in range(len(pdf)):
                    page = pdf[page_num]
                    for img_index, img in enumerate(page.get_images(full=True)):
                        xref = img[0]
                        base_image = pdf.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_filename = f"output_image_page{page_num + 1}_img{img_index + 1}.png"
                        with open(image_filename, "wb") as f:
                            f.write(image_bytes)
            else:

                doc = pdf 
                output_pdf = 'pdf_urez.pdf'

                # Создаем новый PDF-документ
                new_doc = fitz.open()

                # Добавляем страницы из указанного диапазона
                for page_num in range(start_page - 1, end_page):
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

                # Сохраняем новый PDF
                new_doc.save(output_pdf)
                new_doc.close()
                doc.close()

                print(f"Страницы с {start_page} по {end_page} сохранены в {output_pdf}.")



            pdf.close()

        elif programma_obrabotki == 3:  # pdfplumber
            with pdfplumber.open(file_pdf) as pdf:
                if method_obrabotki == 1:  # Извлечь текст
                    text = "".join([page.extract_text() for page in pdf.pages])
                    save_result("output_text.txt", text)
                elif method_obrabotki == 2:  # Извлечь таблицы
                    for page_num, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        for table_num, table in enumerate(tables):
                            save_result(f"output_table_page{page_num + 1}_table{table_num + 1}.txt", str(table))

        elif programma_obrabotki == 4:  # PyPDF4
            if method_obrabotki == 4:  # Урезать документ
                reader = PdfFileReader(file_pdf)
                writer = PdfFileWriter()
                start_page, end_page = 0, 2  # Пример диапазона страниц
                for i in range(start_page, end_page):
                    writer.add_page(reader.getPage(i))
                save_result("output_trimmed.pdf", writer, is_pdf=True)

        elif programma_obrabotki == 5:  # PDFMiner
            if method_obrabotki == 1:  # Извлечь текст
                text = extract_text(file_pdf)
                save_result("output_text.txt", text)

    except Exception as e:
        print(f"Ошибка обработки: {str(e)}")

def save_result(filename, content, is_pdf=False):
    if is_pdf:
        with open(filename, "wb") as file:
            content.write(file)
    else:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

# Пример вызова
file_pdf = "ASME Sec II-D-Metric.pdf"
programma_obrabotki = 2  # PyMuPDF (fitz)
method_obrabotki = 1  # Извлечь текст
dejstvie(file_pdf, programma_obrabotki, method_obrabotki)
