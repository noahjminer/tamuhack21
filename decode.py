from sklearn.preprocessing import MinMaxScaler
from scipy.io.wavfile import write as wavWrite

class Decode:
    def __init__(self, imageFname):
        self.imageFname = imageFname
        self.extractDataFromImage()
        self.denormalize()
    

    # todo - need to extract the normalized wav data, sample rate, scalerMin, and scalerScale from image
    def extractDataFromImage(self): # Possibly add parameter for which function was used to generate image (linear, spiral)
        self.normWavData = [[-1, -1], [-1, -1]]
        self.sampleRate = -1
        self.scalerMin = [-1, -1]
        self.scalerScale = [-1, -1]
    

    # Denormalize extracted wav data and store raw wav data
    def denormalize(self):
        # the feature range will not change
        scaler = MinMaxScaler((0, 1))
        scaler.min_ = self.scalerMin
        scaler.scale_ = self.scalerScale
        self.rawWavData = scaler.inverse_transform(self.normWavData)


    # Export song to current working directory
    def exportSong(self):
        wavWrite(self.imageFname.split('.')[0] + '.wav', self.sampleRate, self.rawWavData)


# dec = Decode('Panis.png')
# dec.exportSong