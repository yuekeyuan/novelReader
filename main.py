#coding=utf-8
from PyQt4 import QtGui, QtCore, Qt
from BodyLayer import *
import json, os, sys
from Tools import *
class MainUI(QtGui.QWidget):

    MAX_SIZE = 1
    MIN_SIZE = 2
    MID_SIZE = 3

    config = None
    def __init__(self, parent = None):
        super(MainUI, self).__init__(parent, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.header = None
        self.body = None
        self.footer = None
        self.title = None
        self.preInitConfig()
        self.config = initConfigInfo()
        self.initUI()
        self.loadFile(self.config["fileName"])
    def initUI(self):
        self.setFixedSize(self.config["mainUi"]["width"], self.config["mainUi"]["height"])
        self.createBody()
        self.createHeader()
        self.createFooter()
        self.createMenu()
        self.header.move(self.config["mainUi"]["head"]["x"], self.config["mainUi"]["head"]["y"])
        self.body.move(self.config["mainUi"]["body"]["x"], self.config["mainUi"]["body"]["y"])
        self.footer.move(self.config["mainUi"]["foot"]["x"], self.config["mainUi"]["foot"]["y"])
        self.menu.move(self.config["mainUi"]["menu"]["x"], self.config["mainUi"]["menu"]["y"])
        self.footer.hide()

    def preInitConfig(self):
        f = open("config.json", "r")
        self.config = json.load(f)

        if "preInit" in self.config and self.config["preInit"] == "false":
            self.config["preInit"] = "true"
            #deskTop
            deskTop = QtGui.QApplication.desktop()
            self.config["deskTop"]["width"] = deskTop.size().width()
            self.config["deskTop"]["height"] = deskTop.size().height()
            #mainUi
            self.config["mainUi"]["x"] = 0
            self.config["mainUi"]["y"] = 0
            self.config["mainUi"]["width"] = int(self.config["deskTop"]["width"] /2 )
            self.config["mainUi"]["height"] = int(self.config["deskTop"]["height"] / 2)
            ##head
            self.config["mainUi"]["head"]["x"] = 0
            self.config["mainUi"]["head"]["y"] = 0
            self.config["mainUi"]["head"]["width"] = self.config["mainUi"]["width"]
            self.config["mainUi"]["head"]["height"] = 30
            ####closeButton
            self.config["mainUi"]["head"]["closeButton"]["width"] = 30
            self.config["mainUi"]["head"]["closeButton"]["height"] = 30
            self.config["mainUi"]["head"]["closeButton"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"]
            self.config["mainUi"]["head"]["closeButton"]["y"] = 0
            ####maxminButton
            self.config["mainUi"]["head"]["maxminButton"]["width"] = 30
            self.config["mainUi"]["head"]["maxminButton"]["height"] = 30
            self.config["mainUi"]["head"]["maxminButton"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"] * 2
            self.config["mainUi"]["head"]["maxminButton"]["y"] = 0
            ####settingButton
            self.config["mainUi"]["head"]["settingButton"]["width"] = 30
            self.config["mainUi"]["head"]["settingButton"]["height"] = 30
            self.config["mainUi"]["head"]["settingButton"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"] * 3
            self.config["mainUi"]["head"]["settingButton"]["y"] = 0
            ##foot
            self.config["mainUi"]["foot"]["x"] = 0
            self.config["mainUi"]["foot"]["y"] = self.config["mainUi"]["height"] - self.config["mainUi"]["foot"]["height"]
            self.config["mainUi"]["foot"]["width"] = self.config["mainUi"]["head"]["width"]
            self.config["mainUi"]["foot"]["height"] = self.config["mainUi"]["head"]["height"]
            ##menu
            self.config["mainUi"]["menu"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"] * 3
            self.config["mainUi"]["menu"]["y"] = 30
            self.config["mainUi"]["menu"]["width"] = 90
            self.config["mainUi"]["menu"]["height"] = 90
            ##body
            self.config["mainUi"]["body"]["x"] = 0
            self.config["mainUi"]["body"]["y"] = self.config["mainUi"]["head"]["height"]
            self.config["mainUi"]["body"]["width"] = self.config["mainUi"]["width"]
            self.config["mainUi"]["body"]["height"] = self.config["mainUi"]["height"] - self.config["mainUi"]["head"]["height"]
        f.close()
        f = open("config.json", "w")
        json.dump(self.config, f, indent=4)
        f.close()

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.config["mainUi"]["background-color"][0],\
            self.config["mainUi"]["background-color"][1],\
            self.config["mainUi"]["background-color"][2],\
            self.config["mainUi"]["background-color"][3])
        painter.fillRect(self.rect(), color)

    def createHeader(self):
        self.header = Header(self.config["mainUi"]["head"], self)
    def createBody(self):
        self.body = Body(self.config["mainUi"]["body"], self)
    def createFooter(self):
        self.footer = Foot(self.config["mainUi"]["head"], self)
    def createMenu(self):
        self.menu = Menu(self.config["mainUi"]["menu"], self)
        self.menu.hide()


    def changeAppSize(self, sizeType):
        if sizeType == self.MAX_SIZE:
            pass
        elif sizeType == self.MID_SIZE:
            pass
        else:
            pass

    def keyReleaseEvent(self, QKeyEvent):
        event = (QtGui.QKeyEvent)(QKeyEvent)
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            sys.exit(0)
        elif key == QtCore.Qt.Key_Up:
            print("up")
        elif key == QtCore.Qt.Key_Down:
            print("down")
        elif key == QtCore.Qt.Key_Left:
            self.body.body.previousPage()
        elif key == QtCore.Qt.Key_Right:
            self.body.body.nextPage()

    def loadFile(self, fileName):
        self.fileName = fileName
        self.setFileName(self.fileName)
        self.setFileContent(self.fileName)

    def setFileName(self, fileName):
        self.fileName = fileName
        if self.header != None:
            self.header.setFileName(fileName)

    def setFileContent(self, fileName):
        pass

    def showMenu(self, status=True):
        if status:
            self.menu.show()
        else:
            self.menu.hide()

    def resetProperties(self, types):
        #TODO: 这一个目前还不是太明朗，嗯嗯，先写其他的，以后再补上这一个。
        pass

    def closeApp(self):
        App.quit()

class Header(QtGui.QWidget):
    #TODO: 实现showMenu信号的发送
    def __init__(self, j = None, parent = None):
        super(Header, self).__init__(parent)
        self.config = j
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.originPos = None
        self.isPressed = False
        self.progress = 1.0
        layout = QtGui.QHBoxLayout(self)
        self.titleLabel = QtGui.QLabel()
        self.titleLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.titleLabel.hide()
        layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.addWidget(self.titleLabel)
        self.setLayout(layout)
        self.closeButton = CloseButton(self.config["closeButton"], self)
        self.menuButton = MenuButton(self.config["settingButton"], self)
        self.closeButton.clicked.connect(self.parent().closeApp)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.config["background-color"][0],\
            self.config["background-color"][1],\
            self.config["background-color"][2],\
            self.config["background-color"][3])
        painter.fillRect(self.rect(), color)

        if self.title:
            print("run to here")
            #TODO: this need to e simplified
            font = self.font()
            font.setPointSize(20)
            self.setFont(font)
            metrix = QtGui.QFontMetrics(font)
            length = metrix.width(self.title)
            if length > self.rect().width():
                x = int((self.rect().width() - 100) / (length / len(self.title)))
                self.title = self.title[0:x]
            pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            pen.setWidth(40)
            painter.setPen(pen)
            print(self.title)
            painter.drawText(QtCore.QPoint(25, 25), self.title)

        #draw the progress bar
        if self.progress:
            painter.fillRect(0, 0, self.progress*self.rect().width(), 2, QtCore.Qt.blue)

    def mousePressEvent(self, QMouseEvent):
        self.isPressed = True
        self.setCursor(QtCore.Qt.SizeAllCursor)
        self.originPos = QMouseEvent.pos()
        print("mousePressed")

    def mouseReleaseEvent(self, QMouseEvent):
        print("run to here")
        self.isPressed = False
        self.setCursor(QtCore.Qt.ArrowCursor)
        print("mouseRelease")

    def mouseMoveEvent(self, QMouseEvent):
        if self.isPressed:
            self.parent().move(QMouseEvent.globalPos() - self.originPos)

    def setFileName(self, title=""):
        #self.title = "<h1 style='font-color:black;text-align:center;margin:0 auto;'>" + title + "</h1>"
        self.title = title
        self.titleLabel.setText(self.title)

class Body(QtGui.QWidget):

    def __init__(self, j, parent = None):
        super(Body, self).__init__(parent)
        self.config = j
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.body = TextLayer(self.config, self)
        self.body.move(0,0)

        self.info = InfoLayer(self.config, self)
        self.info.move(0,0)

        self.mask = MaskLayer(self.config, self)
        self.mask.move(0, 0)


    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(255,0,0,50)
        painter.fillRect(self.rect(), color)

class Foot(QtGui.QWidget):
    def __init__(self, j = None, parent = None):
        super(Foot, self).__init__(parent)
        self.config = j
        self.posX = self.config["x"]
        self.posY = self.config["y"] + self.config["height"]
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.maxminButton = Button(self.config["maxminButton"], self)
        self.settingButton = Button(self.config["settingButton"], self)

    def createCloseButton(self):
        self.closeButton = QtGui.QPushButton(self)
        self.closeButton.setStyleSheet("QPushButton{border:none; background-color:rgb(200,200,200)} QPushButton:hover{border:none; background-color:rgb(0,200,200)}")
        self.closeButton.setFixedSize(self.config["closeButton"]["width"], self.config["closeButton"]["height"])

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.config["background-color"][0],\
            self.config["background-color"][1],\
            self.config["background-color"][2],\
            self.config["background-color"][3])
        painter.fillRect(self.rect(), color)

    direction = 0 #-1 0 1
    signal = 0
    timer = None

    def slide(self):
        if self.direction == -1:
            if self.posY < self.config["height"]:
                self.posY = self.posY - 1
            else:
                self.direction = 0
        if self.direction == 1:
            if self.posY > self.rect().height():
                self.posY = self.posY +1
            else:
                self.direction = 0
        if self.direction != 0:
            self.timer = threading.Timer(0.05, self.slide)

    def slideSignal(self, direction):
        self.direction = direction
        if self.direction != 0:
            self.timer.cancel()
            self.timer = threading.Timer(0.05, self.slide)

class Menu(QtGui.QWidget):
    def __init__(self, j, parent =None):
        super(Menu, self).__init__(parent)
        self.config = j
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.initUi()

    def initUi(self):
        menuClose = Menu.MenuItem(self)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.red)

    def setMenuglobalMenuPosition(self, position):
        #TODO: this is to place the menu on the widget(here we can put it just under the menuButton,so we can do not write code here)
        pass

    class MenuItem(QtGui.QWidget):
        def __init__(self, parent = None):
            super(Menu.MenuItem, self).__init__(parent)
            self.setFixedSize(100,50)
            self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        def paintEvent(self, QPaintEvent):
            painter = QtGui.QPainter(self)
            painter.fillRect(self.rect(), QtCore.Qt.blue)

class Button(QtGui.QPushButton):
    def __init__(self, j, parent = None):
        super(Button, self).__init__(parent)
        self.config = j
        self.isPressed = 0x00  #00,10
        self.isEntered = 0x00  #00,01
        self.setFixedSize(self.config["width"], self.config["height"])
        self.move(self.config["x"], self.config["y"])
        self.initColor()

    def initColor(self):
        self.colorNormal = QtGui.QColor(self.config["background-color"][0],\
            self.config["background-color"][1],\
            self.config["background-color"][2],\
            self.config["background-color"][3])
        self.colorHover = QtGui.QColor(self.config["hover-color"][0],\
            self.config["hover-color"][1],\
            self.config["hover-color"][2],\
            self.config["hover-color"][3])

        self.colorClick = QtGui.QColor(self.config["click-color"][0],\
            self.config["click-color"][1],\
            self.config["click-color"][2],\
            self.config["click-color"][3])

    def paintEvent(self, QPaintEvent):
        status = self.isPressed + self.isEntered
        painter = QtGui.QPainter(self)
        if status == 0:
            painter.fillRect(self.rect(), self.colorNormal)
        elif status == 1:
            painter.fillRect(self.rect(), self.colorHover)
        elif status == 2:
            print("will this kind of case occur?")
        elif status == 3:
            painter.fillRect(self.rect(), self.colorClick)

    def enterEvent(self, *args, **kwargs):
        self.isEntered = 0x01
        self.update()

    def leaveEvent(self, *args, **kwargs):
        self.isEntered = 0x00
        self.update()

    def mousePressEvent(self, *args, **kwargs):
        self.isPressed = 0x02
        self.update()

    def mouseReleaseEvent(self, *args, **kwargs):
        self.isPressed = 0x00
        self.clicked.emit(True)
        self.update()

class CloseButton(Button):
    def __init__(self, j, parent=None):
        super(CloseButton, self).__init__(j, parent)
        self.image = QtGui.QImage("close.png")
    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.drawImage(self.image.rect(), self.image)
        super(CloseButton, self).paintEvent(QPaintEvent)

class MenuButton(Button):
    def __init__(self, j, parent=None):
        super(MenuButton, self).__init__(j, parent)
        self.upImage = QtGui.QImage("up.png")
        self.downImage = QtGui.QImage("down.png")

        self.isMouseEntered = False
        self.isMousePressed = False
        self.isFocusIn      = False
        self.isOutMenuFocusIn = False

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        if self.isMousePressed:
            painter.drawImage(self.downImage.rect(), self.downImage)
        else:
            painter.drawImage(self.upImage.rect(), self.upImage)
        super(MenuButton, self).paintEvent(QPaintEvent)

    def enterEvent(self, *args, **kwargs):
        self.isMouseEntered = True
        self.updateMenuStatus()

    def leaveEvent(self, *args, **kwargs):
        self.isMouseEntered = False
        self.updateMenuStatus()

    def mousePressEvent(self, *args, **kwargs):
        self.isMousePressed = True
        self.updateMenuStatus()

    def mouseReleaseEvent(self, *args, **kwargs):
        self.isMousePressed = False
        self.updateMenuStatus()

    def focusInEvent(self, QFocusEvent):
        self.isFocusIn= True
        self.updateMenuStatus()

    def focusOutEvent(self, QFocusEvent):
        self.isFocusIn = False
        self.updateMenuStatus()

    def setOutMenuFocusStatus(self, status):
        self.isOutMenuFocusIn = status
        self.updateMenuStatus()

    def updateMenuStatus(self):
        pass

if __name__ == "__main__":
    App = QtGui.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("./font/Cousine-Bold.ttf")
    ui = MainUI()
    ui.show()
    App.exec()