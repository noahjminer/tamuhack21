from encode import Encode
from decode import Decode
from imagegenerator import ImageGenerator


# TODO: Link to UI, add directory where images go (optional), add checks for filenames and other variables

class Handler:
    def __init__(self):
        self.active = False
        self.redScalarValue = 1
        self.greenScalarValue = 1
        self.imageToDecode = ""
        self.backgroundImage = ""
        self.wavToEncode = ""

    def encodeWavIntoImage(self, fname, imgOp, bgFname, redScalar, greenScalar):
        if not self.Active:
            self.active = True
            enc = Encode(fname)
            enc.normalize()

            img = ImageGenerator(fname, enc.scalerMin, enc.scalerScale, enc.sampleRate, enc.normWavData,
                imgOp, bgFname, redScalar, greenScalar)
            img.gen_image()
            del enc
            del img
        self.active = False

    def decodeImageIntoWav(self, fname):
        if not self.Active:
            self.active = True
            dec = Decode(fname)
            del dec
        self.active = False


