from sklearn.preprocessing import MinMaxScaler
from scipy.io.wavfile import write as wavWrite
from PIL import Image
from util import list2string
import numpy as np

class Decode:
    def __init__(self, imageFname):
        self.imageFname = imageFname
        self.extractDataFromImage()
        self.denormalize()

    def parseAttributes(self, attributes):
        if len(attributes) != 7:
            print("Incorrect number of attr in extractDataFromImage")
            quit(0)

        self.style = int(list2string(attributes[0]))
        self.wavFilename = list2string(attributes[1])
        self.scalerScale[0] = np.float64(list2string(attributes[2]))
        self.scalerScale[1] = np.float64(list2string(attributes[3]))
        self.scalerMin[0] = np.float64(list2string(attributes[4]))
        self.scalerMin[1] = np.float64(list2string(attributes[5]))
        self.sampleRate = int(list2string(attributes[6]))


    # todo - need to extract the normalized wav data, sample rate, scalerMin, and scalerScale from image
    def extractDataFromImage(self): # Possibly add parameter for which function was used to generate image (linear, spiral)
        self.scalerMin = [-1, -1]
        self.scalerScale = [-1, -1]

        # linear
        with Image.open(self.imageFname) as im:
            pixels = im.getdata()

        # get attributes
        attributes = []
        varArr = []
        whiteCount = 0
        count = 0
        for p in pixels:
            if whiteCount > 7:
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
        self.extractWavData(count, pixels)

    def extractWavData(self, count, pixels):
        self.normWavData = []
        for p in range(count, 960000 + 43):
            lChan = pixels[p][0] / 1000
            rChan = pixels[p][1] / 1000
            # if lChan == 0 and rChan == 0:
            #     break
            self.normWavData.append([lChan, rChan])
        np.array(self.normWavData)


    # Denormalize extracted wav data and store raw wav data
    def denormalize(self):
        scaler = MinMaxScaler((0, 1))
        scaler.min_ = self.scalerMin
        scaler.scale_ = self.scalerScale
        self.rawWavData = scaler.inverse_transform(self.normWavData)


    # Export song to current working directory
    def exportSong(self):
        # print(self.rawWavData, len(self.rawWavData))
        return wavWrite("song.wav", self.sampleRate, np.array(self.normWavData, dtype=float))


dec = Decode('image.png')
dec.exportSong()

print(np.array(dec.normWavData)[0:10], len(dec.normWavData))
# print(np.array(dec.rawWavData)[0:10], len(dec.normWavData))
# print(dec.sampleRate, dec.scalerMin, dec.scalerScale)