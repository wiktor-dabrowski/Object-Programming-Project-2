import Base_classes as Class
import random
import time
import math
from typing import TYPE_CHECKING

import Plants

if TYPE_CHECKING:
	from World import World


class Sheep(Class.Animal):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = 1, strength: int = 4, initiative: int = 4):
		super().__init__(world, x, y, cooldown, strength, initiative)

	def draw(self):
		return "Sheep"


class Wolf(Class.Animal):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = 1, strength: int = 9, initiative: int = 5):
		super().__init__(world, x, y, cooldown, strength, initiative)

	def draw(self):
		return "Wolf"


class Fox(Class.Animal):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = 1, strength: int = 3, initiative: int = 7):
		super().__init__(world, x, y, cooldown, strength, initiative)

	def draw(self):
		return "Fox"

	def _special_action(self, x, y):
		defender = self._world.get_organism(x, y)

		if defender is None:
			return x, y
		else:
			if defender.strength > self._strength:
				return self._x, self._y
			else:
				return x, y


class Turtle(Class.Animal):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = 1, strength: int = 2, initiative: int = 1):
		super().__init__(world, x, y, cooldown, strength, initiative)

	def draw(self):
		return "Turtle"

	def _special_action(self, x, y):
		number = random.randint(0, 3)
		if number < 3:
			return self._x, self._y
		else:
			return x, y

	def _special_collision(self, attacker: Class.Organism):
		if attacker.strength < 5:
			return -2
		else:
			return 0


class Antelope(Class.Animal):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = 1, strength: int = 4, initiative: int = 4):
		super().__init__(world, x, y, cooldown, strength, initiative)

	def draw(self):
		return "Antelope"

	def _special_action(self, x, y):
		return self._where_next(x, y)

	def _special_collision(self, attacker: Class.Organism):
		number = random.randint(0, 1)
		if number == 1:
			x_plus, y_plus = self._find_free(self._x, self._y)
			if x_plus != 0 or y_plus != 0:
				self._x = self._x + x_plus
				self._y = self._y + y_plus
				return -3
		return 0


class CyberSheep(Class.Animal):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = 1000000, strength: int = 11, initiative: int = 4):
		super().__init__(world, x, y, cooldown, strength, initiative)

	def draw(self):
		return "CyberSheep"

	def _special_action(self, x, y):
		length = 0.0
		sos_x = self.x
		sos_y = self.y
		for i in range(self._world.x * self._world.y):
			org_x = i % self._world.x
			i = i // self._world.x
			org_y = i % self._world.y
			organ = self._world.get_organism(org_x, org_y)
			length2 = math.sqrt(pow(org_x - self._x, 2) + pow(org_y - self._y, 2))
			if organ is not None and isinstance(organ, Plants.SosnowskysHogweed):
				if length == 0.0 or length2 < length:
					length = length2
					sos_x = org_x
					sos_y = org_y
		to_return_x, to_return_y = x, y
		if sos_x != self.x or sos_y != self.y:
			x_plus, y_plus = 0, 0
			if sos_x > self.x:
				x_plus = 1
			elif sos_x < self.x:
				x_plus = -1
			if sos_y > self.y:
				y_plus = 1
			elif sos_y < self.y:
				y_plus = -1
			to_return_x = self.x + x_plus
			to_return_y = self.y + y_plus
		return to_return_x, to_return_y


class Human(Class.Animal):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = -5, strength: int = 5, initiative: int = 4):
		super().__init__(world, x, y, cooldown, strength, initiative)

	def __del__(self):
		self._world.special_ability_comm("Człowiek nie żyje")

	def draw(self):
		return "Human"

	def _breed(self, attacker: Class.Organism):
		pass

	def _special_action(self, x, y):
		self._world.draw_a_world()
		while True:
			command = self._world.steering()
			if command == 9:
				if self._cooldown <= -5:
					self._cooldown = 5
					self._world.special_ability_comm("Umiejętność specjalna aktywna ze 100% szansą")
					self._world.set_log("aktywował umiejętność specjalną", self)
			else:
				x_plus, y_plus = self._check_direction(command)
				x = self._x + x_plus
				y = self._y + y_plus
				if self._check_position(x, y):
					break
		if 3 <= self._cooldown <= 5:
			time.sleep(1)
			x, y = self._special_ability(x, y)
		elif 1 <= self._cooldown <= 2:
			if random.randint(0, 1) == 1:
				time.sleep(1)
				x, y = self._special_ability(x, y)
		if self._cooldown == 3:
			self._world.special_ability_comm("Umiejętność specjalna aktywna z 50% szansą")
		elif self._cooldown == 1:
			self._world.special_ability_comm("Umiejętność specjalna nieaktywna")
		elif self._cooldown == -4:
			self._world.special_ability_comm("Umiejętność specjalna gotowa")

		return x, y

	def _special_ability(self, x: int, y: int):
		while True:
			command = self._world.steering()
			x_plus, y_plus = self._check_direction(command)
			to_return_x = x + x_plus
			to_return_y = y + y_plus
			if self._check_position(to_return_x, to_return_y):
				break
		return to_return_x, to_return_y
