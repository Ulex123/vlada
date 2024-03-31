import re

import PyPDF2 as PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTFigure
import csv
import os
from pdf2image import convert_from_path
import pytesseract



def find_text_on_image(element, page):
    image_left, image_bottom, image_right, image_top = element.x0, element.y0, element.x1, element.y1
    page.mediabox.lower_left = (image_left, image_bottom)
    page.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(page)
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

    images = convert_from_path(r'C:\Users\unter\PycharmProjects\VLADA\cropped_image.pdf', poppler_path = r"C:\Program Files\poppler-24.02.0\Library\bin")
    image = images[0]
    image.save('output.png')

    text = pytesseract.image_to_string('output.png', lang='rus')
    return text

with open("avtoref.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(["Путь документа","Автор", "Город", "Год", "Руководитель"])

files = os.listdir(r'avtoreferat')
root = r'C:\Users\unter\PycharmProjects\VLADA\avtoreferat'

for file in files:
    if file.endswith('.pdf'):
        pdf_path = (os.path.join(root, file))
        pdfFileObj = open(pdf_path, 'rb')
        pdfReaded = PyPDF2.PdfReader(pdfFileObj)
        texts = ['', '']
        for pagenum, page in enumerate(extract_pages(pdf_path)):
            pageObj = pdfReaded.pages[pagenum]
            txt = []
            if pagenum == 0 or pagenum == 1:
                texts[pagenum] += pageObj.extract_text()
                for element in page:
                    if isinstance(element, LTFigure):
                        texts[pagenum] += find_text_on_image(element, pageObj)
            else:
                break
        author = re.search('рукописи\s*[А-ЯЁ]\S*\s*[А-ЯЁ]\S+\s*(?:[А-ЯЁ]\S+)', texts[0])
        if author == None:
            author = ['None']
        else:
            author = re.findall(r'[A-ЯЁ]\w+', author[0])
            author = [author[0] + ' ' + author[1]]
        text_for_dateandcity = re.search(r'(Автореферат|АВТОРЕФЕРАТ|автореферат).*', texts[0], re.DOTALL)
        print(text_for_dateandcity)
        # dateandcity = re.search(r'([\n ]{6,}\w*([А-ЯЁ]\w*)(?:[-–—–, \n]*)(\d{4})\s* |([А-ЯЁ]\w*)(?:[-–—–, \n]*)(\d{4})\n*\s*$)', texts[0])
        # if dateandcity == None:
        #     dateandcity = ['None', 'None']
        # else:
        #     dateandcity = re.findall(r'(\w+)(?:[-–—–, \n]*)(\d{4})', dateandcity[0])
        # print(texts)
        # print(dateandcity)
        # pattern_for_rucovoditel = r'(?:руководитель|руководители).*?[А-ЯЁ]\S+\s.*?[А-ЯЁ]\S+\s.*?[А-ЯЁ]\S+'
        # rucovoditel = re.search(pattern_for_rucovoditel, texts[0])
        # if rucovoditel == None:
        #     rucovoditel = re.search(pattern_for_rucovoditel, texts[1])
        # if rucovoditel == None:
        #     rucovoditel = ['None']
        # else:
        #     rucovoditel = re.findall(r'[A-ЯЁ]\w+', rucovoditel[0])
        #     rucovoditel = [rucovoditel[0] + ' ' + rucovoditel[1] + ' ' + rucovoditel[2]]
        # print(texts)
        # print(author[0], dateandcity[0], dateandcity[1], rucovoditel[0])
        # # with open("avtoref.csv", mode="a", encoding='utf-8') as w_file:
        # #     file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        # #     file_writer.writerow([pdf_path, author[0], dateandcity[0], dateandcity[1], rucovoditel])
