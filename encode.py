
from scipy.io.wavfile import read as wavRead
from sklearn.preprocessing import MinMaxScaler

class Encode():


    def __init__(self):
        self.favnumber = 1
    

    def storeWavData(self, wav_fname):
        self.samplerate, self.wavdata = wavRead(wav_fname)
        
    
    def normalizeWavData(self):
        self.scaler = MinMaxScaler((-1, 1))
        self.normalWavData = self.scaler.fit_transform(self.wavdata)


enc = Encode()
enc.storeWavData('Recording.wav')
enc.normalizeWavData()