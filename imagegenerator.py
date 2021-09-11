from PIL import Image
import math


class Pixel:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def getValue(self):
        return (self.r, self.g, self.b)






class ImageGenerator:
    def __init__(self, filename, min, scale, samplerate, data, imageOption=0):
        self.sr = samplerate
        self.data = data
        self.imageOption = imageOption
        self.filename = filename
        self.min = min
        self.scale = scale

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
        for p in self.create_encoded_pixel_string():
            pixelData.append(p)
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

    # Takes necessary wav data and turns into array of Image friendly pixels to decode
    # order is filename, scale, min, samplerate
    # Sequences will be split by extreme value to be determined
    def create_encoded_pixel_string(self):
        pixels = []
        fn = self.filename
        scale = self.scale
        min = self.min
        sr = self.sr

        count = 0

        # start pixel
        pixels.append((1000, 1000, 1000))

        # filename
        tempArray = []
        for i in fn:
            if count < 3:
                count += 1
                tempArray.append(ord(i))
            else:
                count = 1
                p = Pixel(tempArray[0], tempArray[1], tempArray[2])
                pixels.append(p.getValue())
                tempArray.clear()
                tempArray.append(ord(i))


        if count == 3:
            p = Pixel(tempArray[0], tempArray[1], tempArray[2])
            pixels.append(p.getValue())
        elif count == 2:
            p = Pixel(tempArray[0], tempArray[1], 127)
            pixels.append(p.getValue())
        elif count == 1:
            p = Pixel(tempArray[0], 127, 127)
            pixels.append(p.getValue())
        count = 0
        tempArray.clear()

        pixels.append((1000, 1000, 1000))

        for j in scale:
            scaleString = str(j)
            for i in scaleString:
                if count < 3:
                    count += 1
                    tempArray.append(ord(i))
                else:
                    count = 1
                    p = Pixel(tempArray[0], tempArray[1], tempArray[2])
                    pixels.append(p.getValue())
                    tempArray.clear()
                    tempArray.append(ord(i))

            if count == 3:
                p = Pixel(tempArray[0], tempArray[1], tempArray[2])
                pixels.append(p.getValue())
            elif count == 2:
                p = Pixel(tempArray[0], tempArray[1], 127)
                pixels.append(p.getValue())
            elif count == 1:
                p = Pixel(tempArray[0], 127, 127)
                pixels.append(p.getValue())
            count = 0

            pixels.append((1000, 1000, 1000))
        tempArray.clear()

        for k in min:
            minString = str(k)
            for i in minString:
                if count < 3:
                    count += 1
                    tempArray.append(ord(i))
                else:
                    count = 1
                    p = Pixel(tempArray[0], tempArray[1], tempArray[2])
                    pixels.append(p.getValue())
                    tempArray.clear()
                    tempArray.append(ord(i))

            if count == 3:
                p = Pixel(tempArray[0], tempArray[1], tempArray[2])
                pixels.append(p.getValue())
            elif count == 2:
                p = Pixel(tempArray[0], tempArray[1], 127)
                pixels.append(p.getValue())
            elif count == 1:
                p = Pixel(tempArray[0], 127, 127)
                pixels.append(p.getValue())
            count = 0
            pixels.append((1000, 1000, 1000))
        tempArray.clear()

        s = str(sr)
        for i in s:
            if count < 3:
                count += 1
                tempArray.append(ord(i))
            else:
                count = 1
                p = Pixel(tempArray[0], tempArray[1], tempArray[2])
                pixels.append(p.getValue())
                tempArray.clear()
                tempArray.append(ord(i))

        if count == 3:
            p = Pixel(tempArray[0], tempArray[1], tempArray[2])
            pixels.append(p.getValue())
        elif count == 2:
            p = Pixel(tempArray[0], tempArray[1], 127)
            pixels.append(p.getValue())
        elif count == 1:
            p = Pixel(tempArray[0], 127, 127)
            pixels.append(p.getValue())

        pixels.append((1000, 1000, 1000))

        return pixels


