from PIL import ImageDraw, Image, ImageFont, ImageOps


def find_font_size(text, font, image, target_width_ratio):
    tested_font_size = 1
    tested_font = ImageFont.truetype(font, tested_font_size)
    observed_width, observed_height = get_text_size(text, image, tested_font)
    estimated_font_size = tested_font_size / (observed_width / image.width) * target_width_ratio
    return round(estimated_font_size)


def get_text_size(text, image, font):
    im = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(im)
    return draw.textsize(text, font)


def make_text():
    key = True
    while key:
        text = input('Input single or multi line text: ')
        text_size = int(input('Input text size from 0 till 100: '))
        font = input('Input text font: ')
        rotation = int(input('Input rotation in degrees: '))
        opacity = int(input('Input opacity for text from 0 till 255, transparent and not transparent respectively:'))
        position = int(input('Input x: ')), int(input('Input y:'))

        if text == 'q' or text_size == 'q' or rotation == 'q' or opacity == 'q' or position == 'q' or font == 'q' or (not text) or (not text_size) or (not rotation) or (not opacity) or (not position) or (not font):
            key = False
        yield text, text_size, font, rotation, opacity, position

def make_canvas():
    size = int(input('Input width of canvas: ')), int(input('Height of canvas: '))
    background_colour = int(input('Input background colour first: ')), int(input('\rsecond:')), int(input('\rthird: ')), int(input('\rInput transparency from 0 to 255, absolutely transparent and not transparent respectively: '))
    return size, background_colour


def make_watermark():
    canvas = make_canvas()
    image = Image.new('RGBA', size=canvas[0], color=canvas[1])

    for one in make_text():
        text_ = one[0]
        text_size = int(one[1]) / 100
        font_family = one[2]
        angle = one[3]
        text_opacity = one[4]
        position = one[5]

        font_size = find_font_size(text_, font_family, image, text_size)
        font = ImageFont.truetype(font_family, font_size)

        text_layer = Image.new('L', canvas[0])
        draw = ImageDraw.Draw(text_layer)
        draw.text(position, text_, font=font, fill=text_opacity)

        rotated_text_layer = text_layer.rotate(angle, expand=0)
        image.paste(ImageOps.colorize(rotated_text_layer, (0, 0, 0), (255, 255, 255)), (0, 0), rotated_text_layer)

    image.save('WaterMark.png')
    image.show()



make_watermark()
