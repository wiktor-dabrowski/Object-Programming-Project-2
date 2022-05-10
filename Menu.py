# This Python file uses the following encoding: utf-8

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QGraphicsScene
from PyQt5 import uic


class Menu(QWidget):
	def __init__(self):
		super(Menu, self).__init__()
		uic.loadUi("Resources/UI/Menu.ui", self)
		pixmap = QtGui.QPixmap('Resources/IMG/world_picture.jpg')
		pixmap = pixmap.scaled(self.world_picture.width() - 10, self.world_picture.height() - 10, QtCore.Qt.KeepAspectRatio)
		scene = QGraphicsScene()
		scene.addPixmap(pixmap)
		self.world_picture.setScene(scene)
		self.setFixedSize(self.width(), self.height())
