# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("Resources/UI/Window.ui", self)
        self.setWindowTitle("Wiktor Dąbrowski, 184932")
        self.setFixedSize(self.width(), self.height())
