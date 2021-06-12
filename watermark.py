from PIL import ImageDraw, Image, ImageFont
import textwrap
import statistics

# на один символ по горизонтали 0.0165


def craete_watermark(font=None,text_size_cust=1,lines_number=1,rotation=None,direction='ltr',opacity=128,backgrount_as_image=False):

    if not backgrount_as_image:
        size = (1000, 300)     # x, y

        text = "Hello world!!! Привет мир!!! *** ******************"
        max_text_size = int(min(size)*1.65//10)

        if size[0] >= size[1]:
            max_number_char = int((statistics.median(range(size[1],size[0]))+1)//20)

        else:
            max_number_char = 10

        text = textwrap.fill(text, max_number_char)
        lines_number = text.count('\n') + 1

        txt = Image.new("RGBA", size, (255, 255, 255, 0))

        if size[1]//lines_number >= max_text_size//text_size_cust:
            text_size = max_text_size//text_size_cust
        else:
            text_size = size[1]//lines_number

        print(statistics.median(range(size[1],size[0])))
        print(max_number_char)


        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", text_size)

        d = ImageDraw.Draw(txt)

        d.text((0, 0), text, font=font, fill=(0, 0, 0, opacity), direction=direction)

        base = Image.new("RGBA", size, (255, 255, 255, 255))
        out = Image.alpha_composite(base, txt)

        out.show()
    else:
        raise ValueError


craete_watermark()
