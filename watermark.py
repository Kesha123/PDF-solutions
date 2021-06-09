import os
from PIL import ImageDraw, Image, ImageFont

# на один символ по горизонтали 0.0165


def craete_watermark(font=None,text_size_cust=1,lines_number=1,rotation=None,direction='ltr',opacity=128,backgrount_as_image=False):

    if not backgrount_as_image:
        size = (1000, 1000)

        text = input('Input text: ')
        max_text_size = int(min(size)*1.65//10)
        internal_length_of_line = int(min(size)*1.65//len(text))

        if internal_length_of_line < max_text_size:
            for i in range(1,len(text)//10+1):
                text = text[:i*10+1] + '\n' + text[i*10+1:]

        txt = Image.new("RGBA", size, (255, 255, 255, 0))
        text_size = max_text_size//text_size_cust

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", text_size)

        d = ImageDraw.Draw(txt)

        d.text((0, 0), text, font=font, fill=(0, 0, 0, opacity), direction=direction)

        base = Image.new("RGBA", size, (255, 255, 255, 255))
        out = Image.alpha_composite(base, txt)

        out.show()
    else:
        raise ValueError


craete_watermark()
