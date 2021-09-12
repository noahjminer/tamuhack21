from encode import Encode
from decode import Decode
from imagegenerator import ImageGenerator


# TODO: Link to UI, add directory where images go (optional), add checks for filenames and other variables

class Handler:
    def __init__(self):
        self.active = False
        self.style = 0
        self.redScalarValue = 1
        self.greenScalarValue = 1
        self.imageToDecode = ""
        self.backgroundImage = ""
        self.useBg = False
        self.wavToEncode = ""

    def encodeWavIntoImage(self):
        if not self.active:
            self.active = True
            enc = Encode(self.wavToEncode)
            enc.normalize()

            img = ImageGenerator(self.wavToEncode, enc.scalerMin, enc.scalerScale, enc.sampleRate, enc.normWavData,
                self.style, self.backgroundImage, self.redScalarValue, self.greenScalarValue)
            img.gen_image()
            del enc
            del img
        self.active = False

    def decodeImageIntoWav(self):
        if not self.active:
            self.active = True
            dec = Decode(self.imageToDecode)
            dec.exportSong()
            del dec
        self.active = False


