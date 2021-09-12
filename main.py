from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFileDialog)
from PyQt5.QtGui import QPixmap
from handler import Handler


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        self.handler = Handler()

        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        QApplication.setStyle(QStyleFactory.create("Windows"))

        self.complete = QLabel()

        self.complete2 = QLabel()

        styleComboBox = QComboBox()
        styleComboBox.addItems(["Linear", "Spiral"])

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        # top left
        self.le = QLabel()
        self.le2 = QLabel()
        self.embedUpload = QLabel()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()


        styleComboBox.activated[int].connect(self.changeStyle)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        #mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Digital Vinyl")
        # self.changeStyle('Windows')

    def changeStyle(self, styleName):
        self.handler.style = styleName

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Convert wav to image")

        btn = QPushButton("Upload Audio File")
        btn.clicked.connect(self.getfile)

        # fileUpload = QFileDialog()
        # fileUpload.setAcceptMode(QFileDialog.AcceptOpen)
        # fileUpload.setFilter("Audio Files (*.wav)")

        checkBox = QCheckBox("Use background image")
        checkBox.setCheckState(Qt.Unchecked)

        btn2 = QPushButton("Upload Background Image File")
        btn2.clicked.connect(self.getimagefile)

        layout = QVBoxLayout()
        layout.addWidget(self.le)
        layout.addWidget(self.le2)
        layout.addWidget(btn)
        layout.addWidget(btn2)
        self.le2.setFixedSize(200, 200)
        self.le.setBuddy(btn)
        self.le2.setBuddy(btn2)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', "Audio Files (*.wav)")
        self.le.setText(fname[0].split("/")[-1])
        self.handler.wavToEncode = fname[0]

    def getimagefile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image File (*.jpg *.png *.jpeg)')
        self.handler.backgroundImage = fname[0]
        self.le2.setPixmap(QPixmap(fname[0]))

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Render image")

        render = QPushButton("Render")
        render.setDefault(False)
        render.clicked.connect(self.renderImage)

        self.redScalarSlider = QSlider(Qt.Horizontal, self.topRightGroupBox)
        self.redScalarSlider.setTickInterval(1)
        self.redScalarSlider.setMinimum(1)
        self.redScalarSlider.setMaximum(10)
        self.redScalarSlider.valueChanged.connect(self.redscalarchange)
        self.redScalarSlider.setTickPosition(QSlider.TicksBelow)
        self.redScalarSlider.setTickInterval(1)

        self.redScalar = QLabel()
        self.redScalar.setText("Red Scaler: ")
        self.redScalar.setBuddy(self.redScalarSlider)

        self.greenScalarSlider = QSlider(Qt.Horizontal, self.topRightGroupBox)
        self.greenScalarSlider.setTickInterval(1)
        self.greenScalarSlider.setMinimum(1)
        self.greenScalarSlider.setMaximum(10)
        self.greenScalarSlider.setTickPosition(QSlider.TicksBelow)
        self.greenScalarSlider.setTickInterval(1)
        self.greenScalarSlider.valueChanged.connect(self.greenscalarchange)

        self.greenScalar = QLabel()
        self.greenScalar.setText("Green Scaler: ")
        self.greenScalar.setBuddy(self.greenScalarSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.redScalar)
        layout.addWidget(self.redScalarSlider)
        layout.addWidget(self.greenScalar)
        layout.addWidget(self.greenScalarSlider)
        layout.addWidget(self.complete)
        layout.addWidget(render)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def redscalarchange(self):
        self.handler.redScalarValue = self.redScalarSlider.value()
        print(self.redScalarSlider.value())

    def greenscalarchange(self):
        self.handler.greenScalarValue = self.greenScalarSlider.value()
        print(self.greenScalarSlider.value())

    def renderImage(self):
        self.complete.setText("")
        err = self.handler.encodeWavIntoImage()
        if err == -1:
            self.complete.setText("No Image Link")
        else:
            self.complete.setText("Image Rendered")

    def createBottomLeftTabWidget(self):
        self.bottomLeftGroupBox = QGroupBox("Extract wav from image")
        btn = QPushButton("Upload song embedded image")
        btn.clicked.connect(self.getencodedfile)

        layout = QVBoxLayout()
        layout.addWidget(self.embedUpload)
        layout.addWidget(btn)
        self.embedUpload.setFixedSize(200, 200)
        self.embedUpload.setBuddy(btn)
        self.bottomLeftGroupBox.setLayout(layout)

    def getencodedfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Image', '', "Image Files (*.png)")
        self.embedUpload.setPixmap(QPixmap(fname[0]))
        self.handler.imageToDecode = fname[0]
        print(fname)


    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Render wav")
        btn = QPushButton("Extract wav")
        btn.clicked.connect(self.extractwav)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(self.complete2)
        self.bottomRightGroupBox.setLayout(layout)

    def extractwav(self):
        self.complete2.setText("")
        err = self.handler.decodeImageIntoWav()
        if err == -1:
            self.complete2.setText("No audio file inputted")
        else:
            self.complete2.setText("Audio rendered")

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
