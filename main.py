from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFileDialog)
from PyQt5.QtGui import QPixmap


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        QApplication.setStyle(QStyleFactory.create("Windows"))

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

        # top right
        self.greenScalarSlider = QSlider(Qt.Horizontal)
        self.redScalarSlider = QSlider(Qt.Horizontal)

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

        self.setWindowTitle("Styles")
        # self.changeStyle('Windows')

    def changeStyle(self, styleName):
        # switch for style
        print(styleName)

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
        print(fname)

    def getimagefile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image File (*.jpg, *.png)')
        self.le2.setPixmap(QPixmap(fname[0]))
        print(fname)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Render image")

        render = QPushButton("Render")
        render.setDefault(False)
        render.clicked.connect(self.renderImage)

        redScalarSlider = QSlider(Qt.Horizontal, self.topRightGroupBox)
        redScalarSlider.setTickInterval(10)
        redScalarSlider.setMinimum(1)
        redScalarSlider.setMaximum(10)
        redScalarSlider.valueChanged.connect(self.redscalarchange)

        redScalar = QLabel()
        redScalar.setText("Red Scalar: ")
        redScalar.setBuddy(redScalarSlider)

        greenScalarSlider = QSlider(Qt.Horizontal, self.topRightGroupBox)
        greenScalarSlider.setTickInterval(10)
        greenScalarSlider.setMinimum(1)
        greenScalarSlider.setMaximum(10)
        greenScalarSlider.valueChanged.connect(self.greenscalarchange)

        greenScalar = QLabel()
        greenScalar.setText("Green Scalar: ")
        greenScalar.setBuddy(greenScalarSlider)

        layout = QVBoxLayout()
        layout.addWidget(redScalar)
        layout.addWidget(redScalarSlider)
        layout.addWidget(greenScalar)
        layout.addWidget(greenScalarSlider)
        layout.addWidget(render)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def redscalarchange(self):
        print(self.redScalarSlider.value())

    def greenscalarchange(self):
        print(self.greenScalarSlider.value())

    def renderImage(self):
        print("render image")

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
        #self.embedUpload.setText(fname[0].split("/")[-1])
        self.embedUpload.setPixmap(QPixmap(fname[0]))
        print(fname)


    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Render wav")
        btn = QPushButton("Extract wav")
        btn.clicked.connect(self.extractwav)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        self.bottomRightGroupBox.setLayout(layout)

    def extractwav(self):
        print("extract wav")

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
