from PyQt5.QtWidgets import QPushButton, QMenu
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from World import World


class AddButton(QPushButton):
	def __init__(self, world: 'World', x, y):
		super(AddButton, self).__init__()
		self.world = world
		self.x = x
		self.y = y
		menu = QMenu()
		data = [
			"Antelope", "CyberSheep", "Fox", "Sheep", "Turtle", "Wolf",
			"Dandelion", "Grass", "Guarana", "WolfBerries", "SosnowskysHogweed",
		]
		for name in data:
			menu.addAction(name)
		menu.triggered.connect(lambda to_add_name: world.add_organism_by_name(to_add_name.text(), self.x, self.y))
		self.setMenu(menu)
