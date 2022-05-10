import random
import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from World import World


class Organism(abc.ABC):
	def __init__(self, world: 'World', x: int, y: int, strength: int = 0, initiative: int = 0):
		self._strength, self._initiative = strength, initiative
		self._x, self._y = x, y
		self._world = world

	@property
	def initiative(self):
		return self._initiative

	@property
	def strength(self):
		return self._strength

	@strength.setter
	def strength(self, strength: int):
		if strength < 0:
			self._strength = 0
		else:
			self._strength = strength

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, x: int):
		if x < 0:
			self._x = 0
		elif x > self._world.x - 1:
			self._x = self._world.x - 1
		else:
			self._x = x

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, y: int):
		if y < 0:
			self._y = 0
		elif y > self._world.y - 1:
			self._y = self._world.y - 1
		else:
			self._y = y

	@abc.abstractmethod
	def action(self):
		pass

	@abc.abstractmethod
	def collision(self, attacker: 'Organism'):
		pass

	@abc.abstractmethod
	def draw(self):
		pass

	def _check_position(self, x: int, y: int):
		return 0 <= x < self._world.x and 0 <= y < self._world.y

	@staticmethod
	def _check_direction(direction: int):
		x_plus, y_plus = 0, 0
		if direction == 0:
			x_plus, y_plus = 1, 0
		elif direction == 1:
			x_plus, y_plus = 1, 1
		elif direction == 2:
			x_plus, y_plus = 0, 1
		elif direction == 3:
			x_plus, y_plus = -1, 1
		elif direction == 4:
			x_plus, y_plus = -1, 0
		elif direction == 5:
			x_plus, y_plus = -1, -1
		elif direction == 6:
			x_plus, y_plus = 0, -1
		elif direction == 7:
			x_plus, y_plus = 1, -1
		return x_plus, y_plus

	def _where_next(self, x: int, y: int):
		x_plus, y_plus = 0, 0
		tab = [0, 1, 2, 3, 4, 5, 6, 7]
		random.shuffle(tab)
		for i in tab:
			x_plus, y_plus = self._check_direction(i)
			if self._check_position(x + x_plus, y + y_plus):
				break
			x_plus, y_plus = 0, 0
		return x + x_plus, y + y_plus

	def _find_free(self, x: int, y: int):
		x_plus, y_plus = 0, 0
		tab = [0, 1, 2, 3, 4, 5, 6, 7]
		random.shuffle(tab)
		for i in tab:
			x_plus, y_plus = self._check_direction(i)
			if self._check_position(x + x_plus, y + y_plus) and \
					self._world.get_organism(x + x_plus, y + y_plus) is None:
				break
			x_plus, y_plus = 0, 0
		return x_plus, y_plus


class Plant(Organism, abc.ABC):
	def __init__(self, world: 'World', x: int, y: int,
				 strength: int = 0, initiative: int = 0, chance_of_spread: int = 5):
		super().__init__(world, x, y, strength, initiative)
		self._chance_of_spread = chance_of_spread

	@property
	def chance_of_spread(self):
		return self._chance_of_spread

	def action(self):
		self._special_action()
		self._spread()

		return False

	def collision(self, attacker: Organism):
		if self._special_collision(attacker):
			return 2  # plant dies and kills attacker
		else:
			return 1  # plant dies

	@abc.abstractmethod
	def draw(self):
		pass

	def _spread(self):
		if random.randint(1, 100) <= self._chance_of_spread:
			x_plus, y_plus = self._find_free(self._x, self._y)
			if x_plus != 0 or y_plus != 0:
				self._world.add_organism(self._x + x_plus, self._y + y_plus, self)

	def _special_action(self):
		pass

	def _special_collision(self, attacker: Organism):
		return False


class Animal(Organism, abc.ABC):
	def __init__(self, world: 'World', x: int, y: int, cooldown: int = 1, strength: int = 0, initiative: int = 0):
		super().__init__(world, x, y, strength, initiative)
		self._cooldown = cooldown

	@property
	def cooldown(self):
		return self._cooldown

	def action(self):
		new_x, new_y = self._where_next(self._x, self._y)
		new_x, new_y = self._special_action(new_x, new_y)
		self._cooldown -= 1
		if new_x != self._x or new_y != self._y:
			defender = self._world.get_organism(new_x, new_y)
			if defender is None:
				result = -2
			else:
				result = defender.collision(self)

			if result == -2:  # attacker moves and doesnt kill anyone
				self._world.set_log("poruszył się na pole " + str(new_x) + " " + str(new_y), self)
				self._world.move_organism(self._x, self._y, new_x, new_y)
			elif result == -1:  # nobody dies and nobody moves
				self._world.set_log("nie poruszył się", self)
				pass
			elif result == 0:  # attacker is killed
				self._world.set_log("zginął atakując " + defender.draw(), self)
				return True
			elif result == 1:  # attacker kills defender
				self._world.set_log("poruszył się na pole " + str(new_x) + " " + str(new_y)
									+ " i zabił " + defender.draw(), self)
				self._world.kill_organism(new_x, new_y)
				self._world.move_organism(self._x, self._y, new_x, new_y)
				return False
			elif result == 2:  # attacker and defender kill yourselves
				self._world.set_log("zginął po zjedzeniu " + defender.draw(), self)
				self._world.kill_organism(new_x, new_y)
				return True

	def collision(self, attacker: Organism):
		if isinstance(attacker, type(self)):
			self._world.set_log("Powstało nowe życie " + attacker.draw(), self)
			self._breed(attacker)
			return -1
		else:
			result = self._special_collision(attacker)
			if result == 0:  # nothing happens, goes to strength comparison
				if attacker.strength >= self._strength:
					self._world.set_log("został zabity przez " + attacker.draw(), self)
					return 1
				else:
					return 0
			elif result == 1:  # attacker kills defender
				self._world.set_log("został zabity przez " + attacker.draw(), self)
				return 1
			elif result == -1:  # attacker is killed by defender
				return 0
			elif result == -2:  # nobody dies and nobody moves
				return -1
			elif result == -3:  # moves but nobody dies
				return -2
			return -1

	@abc.abstractmethod
	def draw(self):
		pass

	def _breed(self, attacker: Organism):
		if self._cooldown <= 0 and type(attacker) is type(self):
			x_plus, y_plus = self._find_free(self._x, self._y)
			if x_plus != 0 or y_plus != 0:
				child_x, child_y = self._x + x_plus, self._y + y_plus
				self._world.add_organism(child_x, child_y, self)
				self._cooldown = 5

	def _special_action(self, x, y):
		return x, y

	def _special_collision(self, attacker: Organism):
		return 0  # nothing happens and collision goes to normal fight
