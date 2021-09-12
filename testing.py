from encode import Encode
enc = Encode('nirvana.wav')
from imagegenerator import ImageGenerator
gen = ImageGenerator('nirvana.wav', enc.scalerMin, enc.scalerScale, enc.sampleRate, enc.normWavData, 0)
from decode import Decode
dec = Decode('image.png')
dec.exportSong()

# print(np.array(dec.normWavData)[0:10], len(dec.normWavData))
# print(np.array(dec.rawWavData)[0:10], len(dec.rawWavData))
# print(dec.sampleRate, dec.scalerMin, dec.scalerScale)