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
        if len(attributes) != 8:
            print("Incorrect number of attr in extractDataFromImage")
            quit(0)

        self.style = int(list2string(attributes[0]))
        self.wavFilename = list2string(attributes[1])
        self.scalerScale[0] = np.float64(list2string(attributes[2]))
        self.scalerScale[1] = np.float64(list2string(attributes[3]))
        self.scalerMin[0] = np.float64(list2string(attributes[4]))
        self.scalerMin[1] = np.float64(list2string(attributes[5]))
        self.sampleRate = int(list2string(attributes[6]))
        self.pixelCount = int(list2string(attributes[7]))


    # todo - need to extract the normalized wav data, sample rate, scalerMin, and scalerScale from image
    def extractDataFromImage(self): # Possibly add parameter for which function was used to generate image (linear, spiral)
        self.scalerMin = [-1, -1]
        self.scalerScale = [-1, -1]

        # linear
        with Image.open(self.imageFname) as im:
            pixels = im.getdata()

        self.numPixels = len(pixels)
        # get attributes
        attributes = []
        varArr = []
        whiteCount = 0
        count = 0
        for p in pixels:
            if whiteCount > 8:
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
        if self.style == 0:
            for p in range(count, self.pixelCount):
                lChan = pixels[p][0]
                rChan = pixels[p][1]
                self.normWavData.append([lChan, rChan])
        elif self.style == 1:
            dim = int(self.numPixels ** .5)
            numPixParsed = 0
            x = count
            y = 0
            dir = 0
            rightBuf = 0
            downBuf = 0
            leftBuf = 0
            topBuf = 1
            while True:
                if numPixParsed == self.pixelCount-count+5:
                    break
                
                i = x + y * dim
                lchan = pixels[i][0]
                rchan = pixels[i][1]
                self.normWavData.append([lchan, rchan])
                if dir == 0:
                    x += 1
                elif dir == 1:
                    y += 1
                elif dir == 2:
                    x -= 1
                elif dir == 3:
                    y -= 1
                
                if dir == 0 and x == dim-1-rightBuf:
                    dir = 1
                    rightBuf += 1
                elif dir == 1 and y == dim-1-downBuf:
                    dir = 2
                    downBuf += 1
                elif dir == 2 and x == 0+leftBuf:
                    dir = 3
                    leftBuf += 1
                elif dir == 3 and y == 0+topBuf:
                    dir = 0
                    topBuf += 1

                numPixParsed += 1


    # Denormalize extracted wav data and store raw wav data
    def denormalize(self):
        scaler = MinMaxScaler((0, 1))
        scaler.min_ = self.scalerMin
        scaler.scale_ = self.scalerScale
        self.rawWavData = scaler.inverse_transform(self.normWavData)

        import math
        for i in range(len(self.rawWavData)):
            self.rawWavData[i][0] = math.floor(self.rawWavData[i][0])
            self.rawWavData[i][1] = math.floor(self.rawWavData[i][1])


    # Export song to current working directory
    def exportSong(self):
        # print(self.rawWavData, len(self.rawWavData))
        return wavWrite("song.wav", self.sampleRate, np.array(self.rawWavData, dtype=np.int16))
