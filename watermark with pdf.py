from PyPDF2 import PdfFileReader, PdfFileWriter
import os

def watermark_pdf(pdf_source, png_source, target):
    pdf_in = open(pdf_source, 'rb')
    pdf_reader = PdfFileReader(pdf_in)
    pdf_writer = PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)

        if (page.get('/Rotate') == 0) or (page.get('/Rotate') == 180):
            page.rotateClockwise(90)
        pdf_writer.addPage(page)

    target_test = '/'.join(
        target.split('/')[0:len(target.split('/')) - 1] + [target.split('/')[-1].split('.')[0] + '_test.pdf'])

    pdf_out = open(target_test, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

    pdf_file = target_test
    watermark = png_source
    merged_file = target + pdf_source.split('/')[-1]

    input_file = open(pdf_file, 'rb')
    input_pdf = PdfFileReader(input_file)

    writer = PdfFileWriter()

    watermark_file = open(watermark, 'rb')
    watermark_pdf = PdfFileReader(watermark_file)
    watermark_page = watermark_pdf.getPage(0)
    '''/home/peperusland/PycharmProjects/test/mix/Manjaro-logo1.pdf'''
    rotated_watermark_file = open(
        f'{"/".join(watermark_file.split("/")[0:len(watermark_file.split("/")) - 1])}/Manjaro-logo1.pdf', 'rb')
    rotated_watermark_pdf = PdfFileReader(rotated_watermark_file)
    rotated_watermark_page = rotated_watermark_pdf.getPage(0)

    for page in range(input_pdf.numPages):
        pdf_page = input_pdf.getPage(page)
        page_angle = pdf_page.get('/Rotate')

        if page_angle == 270:
            pdf_page.mergePage(rotated_watermark_page)
        else:
            pdf_page.mergePage(watermark_page)
        writer.addPage(pdf_page)

    out = open(merged_file, 'wb')
    writer.write(out)

    watermark_file.close()
    input_file.close()

    os.remove(target_test)
