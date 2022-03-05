from PIL import Image
from PIL.PngImagePlugin import PngImageFile as pil


def preview(image):
    if isinstance(image, pil):
        image.show()
    else:
        img = Image.open(image)
        print(type(img))
        img.show()
