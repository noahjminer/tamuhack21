
from scipy.io.wavfile import read as wavRead
from sklearn.preprocessing import MinMaxScaler

# This class stores raw wav data, normalized wav data, the sample rate, and the scaler instance
class Encode:
    def __init__(self, wav_fname):
        self.wav_fname = wav_fname
    

    def storeWavData(self):
        self.samplerate, self.wavdata = wavRead(self.wav_fname)
        
    
    def normalizeWavData(self):
        self.scaler = MinMaxScaler((-1, 1))
        self.normalWavData = self.scaler.fit_transform(self.wavdata)


# Example of how to use this classs
enc = Encode('Recording.wav')
enc.storeWavData()
enc.normalizeWavData()