from PIL import ImageDraw, Image, ImageFont
import textwrap

# на один символ по горизонтали 0.0165


def craete_watermark(font=None,text_size_cust=9,lines_number=1,rotation=None,direction='ltr',opacity=128,backgrount_as_image=False):

    if not backgrount_as_image:
        size = (1000, 1000)     # x, y

        text = '**********'*20
        max_text_size = int(min(size)*1.65//10)

        max_number_char = ...

        text = textwrap.fill(text, max_number_char)
        lines_number = text.count('\n') + 1

        txt = Image.new("RGBA", size, (255, 255, 255, 0))

        if size[1]//lines_number >= max_text_size//text_size_cust:
            text_size = max_text_size//text_size_cust
        else:
            text_size = size[1]//lines_number

        print(text_size)


        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", text_size)

        d = ImageDraw.Draw(txt)

        d.text((0, 0), text, font=font, fill=(0, 0, 0, opacity), direction=direction)

        base = Image.new("RGBA", size, (255, 255, 255, 255))
        out = Image.alpha_composite(base, txt)

        out.show()
    else:
        raise ValueError


craete_watermark()
