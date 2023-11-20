from PIL import Image


class Colour:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f'Colour({self.r},{self.g},{self.b})'

    def __str__(self):
        return repr(self)


def read_image_to_array(file):
    img = Image.open(file,'r')
    w, h = img.size

    pixels = list(Colour(*pixel) for pixel in img.getdata())

    return [pixels[n:(n+w)] for n in range(0, w*h, w)]

def write_array_to_image(pixels, file):
    h = len(pixels)
    w = len(pixels[0])

    img = Image.new('RGB', (w,h))

    out_pix = img.load()
    for y, row in enumerate(pixels):
        for x,color in enumerate(row):
            out_pix[x,y] = (color.r,color.g,color.b)

    img.save(file)