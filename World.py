import Base_classes as Class
import Animals
import Plants

from Window import Window
from Menu import Menu
from Game import Game

from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget

import sys
import keyboard
import random
import json
from operator import attrgetter


class World:
    def __init__(self):
        self.__x: int = 5
        self.__y: int = 5
        self.__round_nr: int = 0
        self.__list: list[Class.Organism] = []
        self.__organisms_to_create_nr: int = 10
        self.__special_ability_communicate: str = "Umiejętność gotowa"
        self.__logs: list[str] = []

        self.__app = QApplication(sys.argv)
        self.__window = Window()

        self.__menu = Menu()
        self.__menu.new_game_button.pressed.connect(self._new_game)
        self.__menu.load_button.pressed.connect(self._load_game)
        try:
            with open("save.json", "r") as file:
                file.close()
        except IOError:
            self.__menu.load_button.setEnabled(False)
        self.__menu.x_read.setValue(self.__x)
        self.__menu.x_read.valueChanged.connect(self._set_x)
        self.__menu.y_read.setValue(self.__y)
        self.__menu.y_read.valueChanged.connect(self._set_y)
        self._set_organisms_number_borders()
        self.__menu.organisms_nr_read.setValue(self.__organisms_to_create_nr)
        self.__menu.organisms_nr_read.valueChanged.connect(self._set_organisms_to_create_nr)
        self.__game = Game(self)

        self.__layout = QStackedLayout()
        self.__layout.addWidget(self.__menu)
        self.__layout.addWidget(self.__game)
        self.__widget = QWidget()
        self.__widget.setLayout(self.__layout)
        self.__window.setCentralWidget(self.__widget)

        self.__window.show()
        self.__app.exec_()

    def __del__(self):
        pass

    @property
    def x(self):
        return self.__x

    def _set_x(self, x: int):
        self.__menu.x_read.setMaximum(40)
        self.__menu.x_read.setMinimum(2)
        self.__x = x
        self._set_organisms_number_borders()

    @property
    def y(self):
        return self.__y

    def _set_y(self, y: int):
        self.__menu.y_read.setMaximum(30)
        self.__menu.y_read.setMinimum(1)
        self.__y = y
        self._set_organisms_number_borders()

    def special_ability_comm(self, comm: str):
        self.__special_ability_communicate = comm
        self.__game.special_ability_status.setText(self.__special_ability_communicate)

    def _set_organisms_to_create_nr(self, nr: int):
        self.__organisms_to_create_nr = nr
        self.__menu.organisms_nr_read.setValue(nr)

    def _set_organisms_number_borders(self):
        self.__menu.organisms_nr_read.setMaximum(self.__x * self.__y)
        self.__menu.organisms_nr_read.setMinimum(1)

    def get_organism(self, x: int, y: int):
        for it in self.__list:
            if it.x == x and it.y == y:
                return it
        return None

    def add_organism(self, x: int, y: int, organ: Class.Organism):
        organ_type = type(organ)
        new_organ = organ_type(self, x, y)
        if isinstance(new_organ, Class.Plant):
            self.__list.append(new_organ)
        else:
            i = 0
            for it in self.__list:
                if it.initiative < new_organ.initiative:
                    break
                i += 1
            self.__list.insert(i, new_organ)

    def add_organism_by_name(self, name: str, x: int, y: int):
        try:
            klass = getattr(Animals, name)
        except AttributeError:
            klass = getattr(Plants, name)
        org = klass(self, x, y)
        self.add_organism(x, y, org)
        self.draw_a_world()

    def kill_organism(self, x: int, y: int):
        i = 0
        for it in self.__list:
            if it.x == x and it.y == y:
                self.__list.pop(i)
                break
            i += 1

    def move_organism(self, x: int, y: int, x1: int, y1: int):
        for it in self.__list:
            if it.x == x and it.y == y:
                it.x = x1
                it.y = y1
                break

    def game(self):
        self.draw_a_world()
        self.__layout.setCurrentIndex(1)
        self.__game.new_turn_button.released.connect(self._make_turn)
        self.__game.save_game_button.pressed.connect(self._save_game)
        self.__game.save_exit_button.pressed.connect(self._save_and_exit)

    def set_log(self, line: str, org: Class.Organism):
        if isinstance(org, Animals.Human):
            self.__logs.append("Człowiek " + line)
            self.__game.logs_text_area.append(self.__logs[len(self.__logs) - 1])

    def draw_a_world(self):
        self.__game.round_number_show.display(self.__round_nr)
        self.__game.special_ability_status.setText(self.__special_ability_communicate)
        for i in range(self.__x):
            for j in range(self.__y):
                self.__game.buttons_table[i][j].setStyleSheet(
                    "color: rgb(59,244,70); border-style: outset; border-width 2px; ")
                self.__game.buttons_table[i][j].setEnabled(True)
        for it in self.__list:
            self.__game.buttons_table[it.x][it.y].setStyleSheet(
                "::menu-indicator{ image: none; }")
            self.__game.buttons_table[it.x][it.y].setStyleSheet(
                "QPushButton{border-image: url(Resources/IMG/" + it.draw() + ".png) 0 0 0 0 stretch stretch}"
                                                                             "QPushButton::menu-indicator{ image: none; }")
            self.__game.buttons_table[it.x][it.y].setEnabled(False)

    def steering(self):
        self.__game.new_turn_button.setEnabled(False)
        self.__game.save_game_button.setEnabled(False)
        self.__game.save_exit_button.setEnabled(False)
        while True:
            if keyboard.is_pressed("right"):
                to_return = 0
                break
            elif keyboard.is_pressed("down"):
                to_return = 2
                break
            elif keyboard.is_pressed("left"):
                to_return = 4
                break
            elif keyboard.is_pressed("up"):
                to_return = 6
                break
            elif keyboard.is_pressed("r"):
                to_return = 9
                break
            elif keyboard.is_pressed("R"):
                to_return = 9
                break
        self.__game.new_turn_button.setEnabled(True)
        self.__game.save_game_button.setEnabled(True)
        self.__game.save_exit_button.setEnabled(True)
        return to_return

    def _make_turn(self):
        for it in self.__list:
            if it.action():
                self.kill_organism(it.x, it.y)
        self.__round_nr += 1
        self.draw_a_world()

    def _new_game(self):
        tab = []
        for i in range(self.__x * self.__y):
            tab.append(i)
        random.shuffle(tab)
        x = tab[0] % self.__x
        tab[0] = tab[0] // self.__x
        y = tab[0] % self.__y
        self._add_organism_without_object(x, y, "Human")
        for i in range(self.__organisms_to_create_nr - 1):
            x = tab[i + 1] % self.__x
            tab[i + 1] = tab[i + 1] // self.__x
            y = tab[i + 1] % self.__y
            self._create_random_organism(x, y)
        self.__game.organisms_table_create(self.__x, self.__y)
        self.__list.sort(key=attrgetter('initiative'), reverse=True)
        self.game()

    def _load_game(self):
        try:
            with open('save.json', encoding='utf-8') as data_file:
                data = json.load(data_file)
                self.__x = data["x"]
                self.__y = data["y"]
                self.__round_nr = data["round_nr"]
                logs = data["logs"]
                temp_human = Animals.Human(self, 0, 0)
                for line in logs:
                    self.set_log(line, temp_human)
                del temp_human
                self.special_ability_comm(data["special_ability_communicate"])
                animal_list = data["list_animals"]
                plants_list = data["list_plants"]
                bool_table: list[list[bool]] = []
                for i in range(self.__x):
                    tmp_list = []
                    for j in range(self.__y):
                        tmp_list.append(False)
                    bool_table.append(tmp_list)
                for it in animal_list:
                    klass = getattr(Animals, it["name"])
                    org = klass(self, it["x"], it["y"], it["cooldown"], it["strength"])
                    self.__list.append(org)
                    if bool_table[org.x][org.y]:
                        raise NameError("Organisms duplicate position")
                    else:
                        bool_table[org.x][org.y] = True
                for it in plants_list:
                    klass = getattr(Plants, it["name"])
                    org = klass(self, it["x"], it["y"])
                    self.__list.append(org)
                data_file.close()
                self.__game.organisms_table_create(self.__x, self.__y)
                self.game()
        except IOError:
            data_file.close()
            raise NameError("Save file corrupted")

    def _save_game(self):
        data = dict()
        data["x"] = self.__x
        data["y"] = self.__y
        data["round_nr"] = self.__round_nr
        data["special_ability_communicate"] = self.__special_ability_communicate
        data["logs"] = self.__logs
        list_animals = []
        list_plants = []
        for it in self.__list:
            temp_dict = dict()
            if isinstance(it, Class.Animal):
                temp_dict["name"] = it.draw()
                temp_dict["x"] = it.x
                temp_dict["y"] = it.y
                temp_dict["cooldown"] = it.cooldown
                temp_dict["strength"] = it.strength
                list_animals.append(temp_dict)
            elif isinstance(it, Class.Plant):
                temp_dict["name"] = it.draw()
                temp_dict["x"] = it.x
                temp_dict["y"] = it.y
                list_plants.append(temp_dict)
        data["list_animals"] = list_animals
        data["list_plants"] = list_plants
        with open('save.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()

    def _save_and_exit(self):
        self._save_game()
        self.__app.quit()

    def _create_random_organism(self, x: int, y: int):
        number = random.randint(0, 99)

        if number < 15:
            organ = Animals.Antelope(self, x, y)
        elif number < 20:
            organ = Animals.CyberSheep(self, x, y)
        elif number < 30:
            organ = Animals.Fox(self, x, y)
        elif number < 45:
            organ = Animals.Sheep(self, x, y)
        elif number < 60:
            organ = Animals.Turtle(self, x, y)
        elif number < 65:
            organ = Animals.Wolf(self, x, y)
        elif number < 70:
            organ = Plants.Dandelion(self, x, y)
        elif number < 80:
            organ = Plants.Grass(self, x, y)
        elif number < 90:
            organ = Plants.Guarana(self, x, y)
        elif number < 95:
            organ = Plants.SosnowskysHogweed(self, x, y)
        else:
            organ = Plants.WolfBerries(self, x, y)
        self.__list.append(organ)

    def _add_organism_without_object(self, x: int, y: int, name: str):
        if name == "Human":
            self.__list.append(Animals.Human(self, x, y))
