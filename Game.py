# This Python file uses the following encoding: utf-8
from Button import AddButton

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsScene
from PyQt5 import uic
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from World import World


class Game(QWidget):
	def __init__(self, world: 'World'):
		super(Game, self).__init__()
		self.world = world
		uic.loadUi("Resources/UI/Game.ui", self)
		self.setFixedSize(self.width(), self.height())

		pixmap = QtGui.QPixmap('Resources/IMG/steering.png')
		pixmap = pixmap.scaled(self.steering_picture.width() - 10, self.steering_picture.height() - 10, QtCore.Qt.KeepAspectRatio)
		scene = QGraphicsScene()
		scene.addPixmap(pixmap)
		self.steering_picture.setScene(scene)

		self.button_size = 384726
		self.buttons_table = []
		self.layout = QGridLayout()
		self.organisms_table.setLayout(self.layout)
		self.organisms_table.setStyleSheet("background-color: rgb(59,244,70)")  # 3BF446

	def organisms_table_create(self, x: int, y: int):
		self.organisms_table.setFixedSize(self.organisms_table.width(), self.organisms_table.height())
		self.button_size = self.organisms_table.width() // x
		if self.organisms_table.height() // y < self.button_size:
			self.button_size = self.organisms_table.height() // y
		for i in range(x):
			temp_list = []
			for j in range(y):
				button = AddButton(self.world, i, j)
				button.setFixedSize(self.button_size, self.button_size)
				temp_list.append(button)
				self.layout.addWidget(button, j, i)
			self.buttons_table.append(temp_list)
