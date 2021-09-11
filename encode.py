
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
        scaler = MinMaxScaler((0, 1))
        normFit = scaler.fit(self.wavData)
        self.scalerMin = normFit.min_
        self.scalerScale = normFit.scale_
        self.normWavData = normFit.transform(self.wavData)



# *** Example of how to use this class ***
enc = Encode('WATCH_OUT_MOOMIN.WAV')

# *** Example of what scalerScale, scalerMin, and sampleRate will look like ***
# *** These need to be saved inside the image somewhere ***
# print(enc.scalerScale)
# [1.9328527e-05 1.9328527e-05]
# print(enc.scalerMin)
# [0.50236774 0.50236774]
# print(enc.sampleRate)
# 48000

# *** Example of how we would use saved min and scale arr to denormalize data ***
sc = MinMaxScaler((0, 1))
sc.min_ = enc.scalerMin
sc.scale_ = enc.scalerScale
denorm = sc.inverse_transform(enc.normWavData)

# *** Output of normalized data, original data, and denormalized data using saved min and scaler ***
# print(enc.normWavData)
# ...
#  [0.50236774 0.50236774]
#  [0.50236774 0.50236774]
#  [0.50242573 0.50242573]]
# print(enc.wavData)
#  ...
#  [0 0]
#  [0 0]
#  [3 3]]
print(type(enc.scalerScale))
print(enc.scalerMin)
print(denorm)
#  ...
#  [0. 0.]
#  [0. 0.]
#  [3. 3.]]
