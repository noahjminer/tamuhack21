# from encode import Encode
# enc = Encode('beatles.wav')

# from imagegenerator import ImageGenerator
# gen = ImageGenerator('beatles.wav', enc.scalerMin, enc.scalerScale, enc.sampleRate, enc.normWavData, 1)

from decode import Decode
dec = Decode('image2.png')
dec.exportSong()

# print(np.array(dec.normWavData)[0:10], len(dec.normWavData))
# print(np.array(dec.rawWavData)[0:10], len(dec.rawWavData))
# print(dec.sampleRate, dec.scalerMin, dec.scalerScale)