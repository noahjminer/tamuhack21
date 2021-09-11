from PIL import Image
import math


class ImageGenerator:
    def __init__(self, filename, min, scale, sampleRate, data, imageOption=0):
        self.sR = sampleRate
        self.data = data
        self.imageOption = imageOption

    def find_dim(self, len): # need to write in a way that gets closer to len
        sqrt = len ** .5
        if sqrt % 1:
            sqrt = math.floor(sqrt + 1)
        return sqrt

    ##
    # Generate Image
    # Saves a generated image, modifying pixel data based off of wav file data
    # style decided which algorithm to use
    # 0 - linear
    #
    ##
    def gen_image(self, style=0):
        count = 0
        dim = self.find_dim(len(self.data))
        pixelData = []
        cols = 0
        rows = 0
        for i in self.data:
            count += 1

            if cols > dim:
                cols = 0
                rows += 1

            r = math.floor(i[0] * 1000)
            g = math.floor(i[1] * 255)
            b = math.floor((count / dim**2) * 255)
            pixelData.append((r, g, b))

        print(dim)

        img = Image.new('RGB', (dim, dim))
        img.putdata(pixelData)
        img.save('image.png')

    def create_encoded_pixel_string(self):
        pixels = []
        return pixels


