import pdf2image
import os, PyPDF2
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops, ImageFilter
from PyPDF2 import PdfFileReader, PdfFileWriter
import shutil
from reportlab.pdfgen import canvas
import fitz


def create_files_in_folder(pdf, target):
    file_name = pdf.split('/')[-1].split('.')[0]
    path = target
    print(file_name,path)
    if PdfFileReader(pdf).getNumPages() <= 100:
        os.mkdir(f'{path}/{file_name}')
        images = pdf2image.pdf2image.convert_from_bytes(open(f'{pdf}', 'rb').read())
        for i in images:
            if i.size[0] <= i.size[1]:
                i.save(f'{path}/{file_name}/{images.index(i) + 1}.png')
            else:
                image = i.transpose(Image.ROTATE_270)
                image.save(f'{path}/{file_name}/{images.index(i) + 1}.png')

    else:
        pdf_f = PdfFileReader(pdf)
        os.mkdir(f'{path}/{file_name}_test')
        os.mkdir(f'{path}/{file_name}')
        for page in range(pdf_f.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf_f.getPage(page))

            output_filename = f"{file_name}_page_{page + 1}.pdf"

            with open(f"{path}/{file_name}_test/{output_filename}", 'wb') as out:
                pdf_writer.write(out)

        pdf_files = os.listdir(f"{path}/{file_name}_test")

        for file in pdf_files[0:10]:
            images = pdf2image.pdf2image.convert_from_bytes(open(f'{path}/{file_name}_test/{file}', 'rb').read())
            for i in images:
                if i.size[0] <= i.size[1]:
                    i.save(f'{path}/{file_name}/{pdf_files.index(file) + 1}.png')
                else:
                    image = i.transpose(Image.ROTATE_270)
                    image.save(f'{path}/{file_name}/{pdf_files.index(file) + 1}.png')

        shutil.rmtree(f'{path}/{file_name}_test')

create_files_in_folder(pdf='/home/peperusland/Документы/Finland/passport-full-scan.pdf',target='/home/peperusland/PycharmProjects/test/mix/loh/htop')
def watermark_pdf(pdf_source, png_source, target):
    ### Rotate pdf pages if it is necessary ###
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

    ### End rotation ###

    ### Watermark pdf file ###
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
    ### End watermarking ###




