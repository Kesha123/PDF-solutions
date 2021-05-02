from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz
from PIL import Image
import os


def create_with_jpg(jpg_source, pdf_source, target):
    ### Rotate pdf pages if it is necessary ###
    pdf_in = open(pdf_source, 'rb')
    pdf_reader = PdfFileReader(pdf_in)
    pdf_writer = PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)

        if (page.get('/Rotate') == 0) or (page.get('/Rotate') == 180):
            page.rotateClockwise(90)
        if (page.get('/Rotate') == 90):
            page.rotateClockwise(180)
        pdf_writer.addPage(page)

    target_test = '/'.join(
        target.split('/')[0:len(target.split('/')) - 1] + [target.split('/')[-1].split('.')[0] + '_test.pdf'])

    pdf_out = open(target_test, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
    ### End rotation ###

    pdf_name = pdf_source.split('/')[-1]
    marker = Image.open(jpg_source)
    im_rgba = marker.copy()
    im_rgba.putalpha(80)
    im_rgba.save(f'{target}/jpg_to_png.png')

    doc_page = PdfFileReader(open(target_test, 'rb'))
    page_size = doc_page.getPage(0).mediaBox[2:4]

    doc = fitz.open(target_test)
    rect = fitz.Rect(0, 0, page_size[0], page_size[1])
    img = open(f'{target}/jpg_to_png.png', 'rb').read()
    for page in doc:
        page.cleanContents()
        page.insert_image(rect, stream=img)
    doc.save(f'{target}/{pdf_name}')

    os.remove(f'{target}/jpg_to_png.png')
    os.remove(target_test)