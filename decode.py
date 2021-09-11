from sklearn.preprocessing import MinMaxScaler
from scipy.io.wavfile import write as wavWrite
from PIL import Image
from util import list2string
import numpy as np

class Decode:
    def __init__(self, imageFname):
        self.imageFname = imageFname
        self.extractDataFromImage(imageFname)
        self.denormalize()

    def parseAttributes(self, attributes):
        if len(attributes) != 6:
            print("Incorrect number of attr in extractDataFromImage")
            quit(0)

        self.wavFilename = list2string(attributes[0])
        self.scalerScale[0] = np.float64(list2string(attributes[1]))
        self.scalerScale[1] = np.float64(list2string(attributes[2]))
        self.scalerMin[0] = float(list2string(attributes[3]))
        self.scalerMin[1] = float(list2string(attributes[4]))
        self.sampleRate = int(list2string(attributes[5]))

    # todo - need to extract the normalized wav data, sample rate, scalerMin, and scalerScale from image
    def extractDataFromImage(self, filename): # Possibly add parameter for which function was used to generate image (linear, spiral)
        self.scalerMin = [-1, -1]
        self.scalerScale = [-1, -1]
        self.normWavData = [[-1, -1], [-1, -1]]
        self.wavFilename = ""

        # linear
        with Image.open(filename) as im:
            pixels = im.getdata()

        # get attributes
        attributes = []
        varArr = []
        whiteCount = 0
        count = 0
        for p in pixels:
            if whiteCount > 6:
                break
            count += 1
            if p == (255, 255, 255):
                whiteCount += 1
                if len(varArr) > 0:
                    attributes.append(varArr.copy())
                    varArr.clear()
                continue
            else:
                varArr.append(p[0])
                varArr.append(p[1])
                varArr.append(p[2])
        self.parseAttributes(attributes)

        for p in range(count, len(pixels)):
            lChan = (pixels[p][0] / 255) * 2 - 1
            rChan = (pixels[p][1] / 255) * 2 - 1
            self.normWavData.append([lChan, rChan])
        np.array(self.normWavData)

    # Denormalize extracted wav data and store raw wav data
    def denormalize(self):
        # the feature range will not change
        scaler = MinMaxScaler((0, 1))
        scaler.min_ = self.scalerMin
        print(self.scalerMin)
        print(self.scalerScale)
        scaler.scale_ = self.scalerScale
        self.rawWavData = scaler.inverse_transform(self.normWavData)
        np.array(self.rawWavData)



    # Export song to current working directory
    def exportSong(self):
        print(self.rawWavData)
        return wavWrite("song.wav", self.sampleRate, self.rawWavData)


# dec = Decode('Panis.png')
# dec.exportSong