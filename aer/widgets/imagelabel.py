from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QKeyEvent
from PyQt5.QtWidgets import QLabel


class ImageLabel(QLabel):

    mousePressed = pyqtSignal(QMouseEvent)
    mouseReleased = pyqtSignal(QMouseEvent)
    mouseMove = pyqtSignal(QMouseEvent)
    wheelScrolled = pyqtSignal(QWheelEvent)
    keyPressed = pyqtSignal(QKeyEvent)

    def __init__(self, *__args):
        super().__init__(*__args)

    def mousePressEvent(self, event):
        self.mousePressed.emit(event)

    def mouseReleaseEvent(self, event):
        self.mouseReleased.emit(event)

    def mouseMoveEvent(self, event):
        self.mouseMove.emit(event)

    def wheelEvent(self, event):
        modifiers = QtGui.QGuiApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            self.wheelScrolled.emit(event)
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        self.keyPressed.emit(event)
