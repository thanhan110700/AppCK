from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
import matplotlib.pyplot as plt
import sys
import numpy as np
import cv2 as cv
from PIL import Image
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import blur,gamma,Hue,histogram,daoanh,saturation

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Clone Photoshop"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 600
        self.InitWindow()
        self.setStyleSheet("background-color:#3F3F3F")
        self.clickbtnDaoanh = 0
        self.hue_value_now = 0
        self.gamma_value_now = 1
        self.blur_value_now = 0
        self.saturation_value_now = 0
        self.filename = None
        self.tmp = None
        self.old_imagePath = "None"
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.createLayout()

        self.show()
    def createLayout(self):

        hboxBig = QHBoxLayout()
        hbox = QHBoxLayout()

        #Button Image
        openImage = QPushButton("Open",self)
        openImage.setStyleSheet("Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
        openImage.clicked.connect(self.getImage)
        saveImage = QPushButton("Save",self)
        saveImage.setStyleSheet("Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
        saveImage.clicked.connect(self.saveImage)
        hbox.addWidget(openImage, 1)
        hbox.addWidget(saveImage,1)
        hbox.addStretch(5)

        vboxLeft = QVBoxLayout()
        vboxLeft.addLayout(hbox)

        # Image
        hboxImage = QHBoxLayout()
        self.lblImage = QLabel()

        self.lblImage.setFixedSize(450, 450)
        self.lblImage.setStyleSheet("border:1px solid white;")
        defaulImage = QPixmap('image/noimg.png')
        scaledefaulImage = defaulImage.scaled(50, 50)
        self.lblImage.setPixmap(scaledefaulImage)
        self.lblImage.setAlignment(Qt.AlignCenter)


        hboxImage.addWidget(self.lblImage)
        hboxImage.setAlignment(Qt.AlignCenter)

        vboxLeft.addLayout(hboxImage)
        hboxBig.addLayout(vboxLeft,2)

        # Show Histogram
        vboxHistgram = QVBoxLayout()
        lblHistogram = QLabel("Histogram")
        lblHistogram.setStyleSheet("color:white")
        self.lblImgHis = QLabel()

        self.lblImgHis.setFixedSize(350,260)
        self.lblImgHis.setStyleSheet("border:1px solid white;")
        vboxHistgram.addWidget(lblHistogram)
        vboxHistgram.addWidget(self.lblImgHis)
        # Temperature
        vboxGamma = QVBoxLayout()
        self.lblNumGamma = QLabel('1')
        self.lblNumGamma.setStyleSheet("color:white")
        self.lblNumGamma.setAlignment(Qt.AlignRight)
        lblGamma = QLabel("Gamma")
        lblGamma.setStyleSheet("color:white")
        self.sliGamma = QSlider(Qt.Horizontal)
        self.sliGamma.setDisabled(True)
        self.sliGamma.setMinimum(-100)
        self.sliGamma.setMaximum(100)

        self.sliGamma.setTickInterval(0)
        self.lblNumGamma.setText(self.sliGamma.value().__str__())
        self.sliGamma.valueChanged.connect(self.value_changed_Gamma)  # Inside __init__() function
        vboxGamma.addWidget(lblGamma)
        vboxGamma.addWidget(self.lblNumGamma)
        vboxGamma.addWidget(self.sliGamma)

        # Saturation
        vboxSaturation = QVBoxLayout()
        self.lblNumSaturation = QLabel('1')
        self.lblNumSaturation.setStyleSheet("color:white")
        self.lblNumSaturation.setAlignment(Qt.AlignRight)
        lblSaturation = QLabel("Saturation")
        lblSaturation.setStyleSheet("color:white")
        self.sliSaturation = QSlider(Qt.Horizontal)
        self.sliSaturation.setDisabled(True)
        self.sliSaturation.setMinimum(-100)
        self.sliSaturation.setMaximum(100)
        self.sliSaturation.setTickInterval(0)

        self.sliSaturation.valueChanged.connect(self.value_changed_Saturation)  # Inside __init__() function
        self.lblNumSaturation.setText(self.sliSaturation.value().__str__())
        vboxSaturation.addWidget(lblSaturation)
        vboxSaturation.addWidget(self.lblNumSaturation)
        vboxSaturation.addWidget(self.sliSaturation)

        # HUE
        vboxHue = QVBoxLayout()
        self.lblNumHue = QLabel('1')
        self.lblNumHue.setStyleSheet("color:white")
        self.lblNumHue.setAlignment(Qt.AlignRight)
        lblHue = QLabel("Hue")
        lblHue.setStyleSheet("color:white")
        self.sliHue = QSlider(Qt.Horizontal)
        self.sliHue.setDisabled(True)
        self.sliHue.setMinimum(-100)
        self.sliHue.setMaximum(100)
        self.sliHue.setTickInterval(0)

        self.sliHue.valueChanged.connect(self.value_changed_Hue)  # Inside __init__() function
        self.lblNumHue.setText(self.sliHue.value().__str__())
        vboxHue.addWidget(lblHue)
        vboxHue.addWidget(self.lblNumHue)
        vboxHue.addWidget(self.sliHue)


        # BLur
        vboxBLur = QVBoxLayout()
        self.lblNumBlur = QLabel('1')
        self.lblNumBlur.setStyleSheet("color:white")
        self.lblNumBlur.setAlignment(Qt.AlignRight)
        lblBlur = QLabel("Blur")
        lblBlur.setStyleSheet("color:white")
        self.sliBlur = QSlider(Qt.Horizontal)
        self.sliBlur.setDisabled(True)
        self.sliBlur.setMinimum(0)
        self.sliBlur.setMaximum(100)
        self.sliBlur.setTickInterval(0)
        self.sliBlur.valueChanged.connect(self.value_changed_Blur)  # Inside __init__() function
        self.lblNumBlur.setText(self.sliBlur.value().__str__())
        vboxBLur.addWidget(lblBlur)
        vboxBLur.addWidget(self.lblNumBlur)
        vboxBLur.addWidget(self.sliBlur)


        # Widget Button
        hboxButton = QHBoxLayout()
        # Đảo ảnh
        self.btnDaoanh = QPushButton("Đảo ảnh")
        self.btnDaoanh.setStyleSheet("Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
        self.btnDaoanh.setCheckable(True)
        self.btnDaoanh.clicked.connect(self.action_daoanh)

        hboxButton.addWidget(self.btnDaoanh,1)
        hboxButton.addStretch(3)
        #  WIDGET
        vboxRight = QVBoxLayout()

        vboxRight.setAlignment(Qt.AlignTop)
        vboxRight.addLayout(vboxHistgram,5)
        vboxRight.addLayout(vboxGamma,1)
        vboxRight.addLayout(vboxHue, 1)
        vboxRight.addLayout(vboxSaturation, 1)
        vboxRight.addLayout(vboxBLur, 1)
        vboxRight.addLayout(hboxButton,1)
        hboxBig.addLayout(vboxRight,1)

        self.setLayout(hboxBig)

    ############# Value Gamma
    def value_changed_Gamma(self,value):

        if(value<0):
            self.gamma_value_now = 1-value*-0.01
            self.lblNumGamma.setText(round(self.gamma_value_now, 1).__str__())
        if(value==0):
            self.gamma_value_now = 1
            self.lblNumGamma.setText(round(self.gamma_value_now , 1).__str__())
        if(value>0):
            self.gamma_value_now = 1+value*0.1
            self.lblNumGamma.setText(round(self.gamma_value_now - 1, 1).__str__())
        self.gamma_value_now = round(self.gamma_value_now,1)


        self.update()

    ############# Value Hue
    def value_changed_Hue(self,value):
        self.hue_value_now = value
        self.lblNumHue.setText(value.__str__())
        self.update()
    def value_changed_Saturation(self,value):
        self.saturation_value_now = value
        self.lblNumSaturation.setText(value.__str__())
        self.update()

    ############# Value Blur
    def value_changed_Blur(self,value):
        self.blur_value_now = value
        self.lblNumBlur.setText(value.__str__())
        self.update()

    #######UPDATE HISTOGRAM
    def update_histogram(self,img):
        image = histogram.histogram(img)
        frame = cv.cvtColor(image, cv.COLOR_BGRA2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        image = image.scaledToHeight(self.lblImgHis.height(), Qt.SmoothTransformation)
        self.lblImgHis.setPixmap(QPixmap.fromImage(image))
    ###### action Dao anh
    def action_daoanh(self):
        if (self.btnDaoanh.isChecked() == True):
            self.btnDaoanh.setStyleSheet(
                "Background-color:#dfe6e9;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:black")
            self.clickbtnDaoanh = 1
        if (self.btnDaoanh.isChecked() == False):
            self.btnDaoanh.setStyleSheet(
                "Background-color:none;border: 1px solid white;border-radius:10px;height:30%;width:25%;color:white")
            self.clickbtnDaoanh = 2
        self.update()    
    def dao(self,img):
        img = daoanh.dao_anh(img)
    def dao_nguoc(self,img):
        img = daoanh.dao_anh_nguoc(img)
    ######UPDATE FUNTION
    def update(self):
        img = gamma.changeGamma(self.im, self.gamma_value_now)
        img = Hue.changeHue(img, self.hue_value_now)
        img = saturation.changeSaturation(img, self.saturation_value_now)
        img = blur.changeBlur(img,self.blur_value_now)
        if(self.clickbtnDaoanh==1):
            img = daoanh.dao_anh(img)
        if(self.clickbtnDaoanh==2):
            img = daoanh.dao_anh_nguoc(img)
            self.clickbtnDaoanh = 0
        self.setImage(img)
    ######## SAVE IMAGE FUNCTION
    def saveImage(self):
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        if(filename!=''):
            cv.imwrite(filename, self.tmp)
            print('Image saved as:', self.filename)
        else:
            print("don't save")

    ########## OPEN IMAGE FUNCTION
    def getImage(self):
        path_img = QFileDialog.getOpenFileName(filter="Image (*.*)")
        imagePath = path_img[0]
        print("old",self.old_imagePath,"path:",imagePath)
        if(path_img[0] != "" and self.old_imagePath=="None"):
            print('1')
            self.old_imagePath = imagePath
            self.filename = imagePath
            self.im = cv.imread(imagePath)
            self.sliBlur.setEnabled(True)
            self.sliGamma.setEnabled(True)
            self.sliSaturation.setEnabled(True)
            self.sliHue.setEnabled(True)
            self.setImage(self.im)
        if (path_img[0] != "" and self.old_imagePath != "None"):

            self.old_imagePath = imagePath
            self.filename = imagePath
            self.im = cv.imread(imagePath)
            self.sliBlur.setTickInterval(0)
            self.sliSaturation.setTickInterval(0)
            self.sliGamma.setTickInterval(0)
            self.sliHue.setTickInterval(0)

            self.setImage(self.im)
        if (path_img[0] == "" and self.old_imagePath != "None"):
            self.update()
        if (path_img[0] == "" and self.old_imagePath == "None"):
            defaulImage = QPixmap('image/noimg.png')
            scaledefaulImage = defaulImage.scaled(50, 50)
            self.lblImage.setPixmap(scaledefaulImage)

    ########### SET IMAGE INTO QLABEL
    def setImage(self,image):
        self.update_histogram(image)
        self.tmp = image
        frame = cv.cvtColor(image,cv.COLOR_BGRA2RGB)
        image = QImage(frame,frame.shape[1],frame.shape[0], frame.strides[0],QImage.Format_RGB888)
        if (image.width() > image.height()):
            image = image.scaledToWidth(self.lblImage.width(), Qt.SmoothTransformation)
            self.lblImage.setPixmap(QPixmap.fromImage(image))
        if (image.width() < image.height()):
            image = image.scaledToHeight(self.lblImage.height(), Qt.SmoothTransformation)
            self.lblImage.setPixmap(QPixmap.fromImage(image))
        else:
            image = image.scaledToWidth(self.lblImage.width(), Qt.SmoothTransformation)
            self.lblImage.setPixmap(QPixmap.fromImage(image))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())