import os
from PIL import ImageDraw, Image, ImageFont

# на один символ по горизонтали 0.0165

def craete_watermark(font=None,text_size=1,lines_number=1,rotation=None,direction='ltr',opacity=128,backgrount_as_image=False):

    if not backgrount_as_image:
        size = 2000, 2000
        max_text_size = int(size[0]*1.65)
        txt = Image.new("RGBA", size, (255, 255, 255, 0))

        text = input('Input text: ')
        text_size = int(size[0]*1.65//len(text))

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", text_size)

        d = ImageDraw.Draw(txt)

        d.text((0, 0), text, font=font, fill=(0, 0, 0, opacity), direction=direction)

        base = Image.new("RGBA", size, (255, 255, 255, 255))
        out = Image.alpha_composite(base, txt)

        out.show()
    else:
        raise ValueError


craete_watermark()
