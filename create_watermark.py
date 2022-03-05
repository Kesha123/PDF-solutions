import os
from PIL import ImageDraw, Image, ImageFont


def create_image(size, text_position, font,direction):
    test = Image.new('RGB', size, (255,255,255))
    img = ImageDraw.Draw(test)
    img.text(text_position, "PREVIEW", font=font, fill=(0, 0, 0),direction=direction)
    test.save('WMIMG.png')

    img = Image.open('WMIMG.png')
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []

    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)

    img_to_convert = img.copy()
    img_to_convert.putalpha(80)
    img_to_convert.save('WM.png')

    os.remove('WMIMG.png')


def params(size,size_for_text):
    if (size[0] > size[1]):
        text_size = min(size_for_text) // 4
        text_position = size[0] // 2 - text_size * 2.5, size[1] // 2 - text_size // 2
        direction = 'ltr'
    elif (size[0] < size[1]):
        text_size = min(size_for_text) // 4
        text_position = (min(size)-text_size)//2, (max(size)-text_size*7)//2
        direction = 'ttb'
    else:
        text_size = min(size_for_text) // int(str(min(size_for_text))[0])
        text_position = size[0] // 2 - text_size * 2.5, size[1] // 2 - text_size // 2
        direction = 'ltr'
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', text_size)

    return size, text_position, font, direction, text_size





