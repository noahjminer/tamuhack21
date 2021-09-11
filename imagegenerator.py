from PIL import Image


class ImageGenerator:
    def __init__(self, sampleRate, data, imageOption=0):
        self.sR = sampleRate
        self.data = data
        self.imageOption = imageOption

    def find_dim(self, len):
        sqrt = len ** .5
        if sqrt % 1:
            sqrt += 1
        return sqrt

    def gen_image(self):
        dim = self.find_dim(len(self.data))
        pixelData = []
        cols = 0
        rows = 0
        for i in self.data:
            if cols > dim:
                cols = 0
                rows += 1

            pixelData.append(i[0])
            cols += 1

            if cols > dim:
                cols = 0
                rows += 1

            pixelData.append(i[1])

        img = Image.new('RGB', (dim, dim))
        img.putdata(pixelData)
        img.save('image.png')


