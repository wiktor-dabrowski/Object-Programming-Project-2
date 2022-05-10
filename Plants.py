import random

import Base_classes as Class
import Animals
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from World import World


class Grass(Class.Plant):
	def __init__(self, world: 'World', x: int, y: int,
				 strength: int = 0, initiative: int = 0, chance_of_spread: int = 10):
		super().__init__(world, x, y, strength, initiative, chance_of_spread)

	def draw(self):
		return "Grass"


class Dandelion(Class.Plant):
	def __init__(self, world: 'World', x: int, y: int,
				 strength: int = 0, initiative: int = 0, chance_of_spread: int = 10):
		super().__init__(world, x, y, strength, initiative, chance_of_spread)

	def draw(self):
		return "Dandelion"

	def _special_action(self):
		self._spread()
		self._spread()


class Guarana(Class.Plant):
	def __init__(self, world: 'World', x: int, y: int,
				 strength: int = 0, initiative: int = 0, chance_of_spread: int = 10):
		super().__init__(world, x, y, strength, initiative, chance_of_spread)

	def draw(self):
		return "Guarana"

	def _special_collision(self, attacker: Class.Organism):
		attacker.strength += 3
		self._world.set_log("zyskał 3 sił dzięki zjedzeniu guarany", attacker)
		return False


class WolfBerries(Class.Plant):
	def __init__(self, world: 'World', x: int, y: int,
				 strength: int = 99, initiative: int = 0, chance_of_spread: int = 10):
		super().__init__(world, x, y, strength, initiative, chance_of_spread)

	def draw(self):
		return "WolfBerries"

	def _special_collision(self, attacker: Class.Organism):
		return True


class SosnowskysHogweed(Class.Plant):
	def __init__(self, world: 'World', x: int, y: int,
				 strength: int = 10, initiative: int = 0, chance_of_spread: int = 5):
		super().__init__(world, x, y, strength, initiative, chance_of_spread)

	def draw(self):
		return "SosnowskysHogweed"

	def _special_action(self):
		tab = [0, 1, 2, 3, 4, 5, 6, 7]
		random.shuffle(tab)
		for i in tab:
			x_plus, y_plus = self._check_direction(i)
			to_kill_x = self._x + x_plus
			to_kill_y = self._y + y_plus
			if self._check_position(to_kill_x, to_kill_y):
				defender = self._world.get_organism(to_kill_x, to_kill_y)
				if defender is not None \
						and not isinstance(defender, Class.Plant) and not isinstance(defender, Animals.CyberSheep):
					self._world.set_log("został zabity przez barszcz", defender)
					self._world.kill_organism(to_kill_x, to_kill_y)

	def _special_collision(self, attacker: Class.Organism):
		if isinstance(attacker, Animals.CyberSheep):
			return False
		else:
			return True
