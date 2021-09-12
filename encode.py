
from scipy.io.wavfile import read as wavRead
from sklearn.preprocessing import MinMaxScaler

# This class stores raw wav data, normalized wav data, the sample rate, scalerMin, scalerScale, and fileName
class Encode:
    def __init__(self, wavFname):
        self.wavFname = wavFname
        self.storeWavData()
        self.normalize()
    

    # Store sample rate and raw wav data
    def storeWavData(self):
        self.sampleRate, self.wavData = wavRead(self.wavFname)
    

    # Normalize data to (0, 1)
    # We need to encode scalermin, scalerscale, and normWavData into the image
    def normalize(self):
        scaler = MinMaxScaler((0, 255))
        normFit = scaler.fit(self.wavData)
        self.scalerMin = normFit.min_
        self.scalerScale = normFit.scale_
        self.normWavData = normFit.transform(self.wavData)
