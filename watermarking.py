from create_watermark import create_image, params
from PIL import ImageDraw, ImageFont, Image


def watermark_png(input_image_path, output_image_path):
    base_image = Image.open(input_image_path)
    width, height = base_image.size

    size = int(height*1.5), int(width*2)
    size_for_text = height, width
    properties = params(size,size_for_text)

    create_image(size=properties[0], text_position=properties[1], font=properties[2], direction=properties[3])

    watermark = Image.open('WM.png')
    watermark = watermark.rotate(45)

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (int(-2*properties[4]), int(-1.5*properties[4])), mask=watermark)
    transparent.save(output_image_path)


watermark_png('/home/pepefinland/PycharmProjects/WM/Rogaljow, Das Beschwerdebuch P/1.png','/home/pepefinland/PycharmProjects/WM/1.png')


